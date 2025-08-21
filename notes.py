#!/usr/bin/env python3
"""
Simple CLI Notes Application with YDB
=====================================

A simple command-line notes application that uses YDB as a database.
Supports creating, listing, viewing, and deleting notes.

Commands:
    init                    - Initialize database and create notes table
    add <title> <content>   - Create a new note
    list                    - Show 5 most recent notes
    show <id>               - Show note content by ID
    delete <id>             - Delete note by ID

Environment Variables:
    YDB_ENDPOINT    - YDB endpoint (default: grpc://localhost:2136)
    YDB_DATABASE    - YDB database path (default: /local)
"""

import argparse
import os
import sys
import uuid
from datetime import datetime

import ydb


class NotesApp:
    """Simple notes application using YDB as storage."""

    def __init__(self, use_env_auth: bool = False):
        """Initialize the notes application.

        Args:
            use_env_auth: If True, use authentication from environment variables
        """
        self.endpoint = os.getenv('YDB_ENDPOINT', 'grpc://localhost:2136')
        self.database = os.getenv('YDB_DATABASE', '/local')
        self.use_env_auth = use_env_auth
        self.driver = None
        self.query_session_pool = None

    def connect(self) -> bool:
        """Connect to YDB database.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create driver configuration with appropriate credentials
            if self.use_env_auth:
                # Use authentication from environment variables
                credentials = ydb.construct_credentials_from_environ()
            else:
                # Use anonymous authentication (no credentials)
                credentials = ydb.AnonymousCredentials()
            
            config = ydb.DriverConfig(
                endpoint=self.endpoint,
                database=self.database,
                credentials=credentials
            )

            # Initialize driver
            self.driver = ydb.Driver(config)
            self.driver.wait(fail_fast=True, timeout=5)

            # Create query session pool for all operations
            self.query_session_pool = ydb.QuerySessionPool(self.driver)

            print(f"✅ Connected to YDB at {self.endpoint}")
            return True

        except Exception as e:
            print(f"❌ Failed to connect to YDB: {e}")
            return False

    def disconnect(self):
        """Disconnect from YDB database."""
        if self.driver:
            self.driver.stop()

    def init_database(self) -> bool:
        """Initialize database and create notes table.

        Returns:
            bool: True if initialization successful, False otherwise
        """
        if not self.connect():
            return False

        try:
            try:
                self.query_session_pool.execute_with_retries("SELECT * FROM notes LIMIT 0")
                print("ℹ️  Table 'notes' already exists")
            except ydb.SchemeError:
                # Table doesn't exist, create it using Data Definition Language
                print("📄 Creating table 'notes'...")
                
                # Create table using DDL syntax - MUST be executed outside transaction
                create_table_query = """
                    CREATE TABLE notes (
                        id Utf8 NOT NULL,
                        title Utf8,
                        content Utf8,
                        created_at Timestamp,
                        updated_at Timestamp,
                        PRIMARY KEY (id)
                    );
                """
                
                # Execute DDL outside transaction as per YDB Query Service requirements
                self.query_session_pool.execute_with_retries(create_table_query)
                print("✅ Table 'notes' created successfully")
            
            # Execute through query session pool (new API) for consistency
            print("🎉 Database initialized successfully!")
            return True

        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            return False
        finally:
            self.disconnect()

    def add_note(self, title: str, content: str) -> bool:
        """Add a new note.

        Args:
            title: Note title
            content: Note content

        Returns:
            bool: True if note added successfully, False otherwise
        """
        if not self.connect():
            return False

        try:
            note_id = str(uuid.uuid4())
            now = datetime.now()

            def insert_note(session):
                # Insert note using query-service
                insert_query = """
                    INSERT INTO notes (id, title, content, created_at, updated_at)
                    VALUES ($id, $title, $content, $created_at, $updated_at);
                """
                
                parameters = {
                    '$id': ydb.TypedValue(note_id, ydb.PrimitiveType.Utf8),
                    '$title': ydb.TypedValue(title, ydb.PrimitiveType.Utf8),
                    '$content': ydb.TypedValue(content, ydb.PrimitiveType.Utf8),
                    '$created_at': ydb.TypedValue(now, ydb.PrimitiveType.Timestamp),
                    '$updated_at': ydb.TypedValue(now, ydb.PrimitiveType.Timestamp),
                }

                session.transaction().execute(insert_query, parameters, commit_tx=True)

            self.query_session_pool.retry_operation_sync(insert_note)
            print(f"✅ Note created with ID: {note_id}")
            return True

        except Exception as e:
            print(f"❌ Failed to add note: {e}")
            return False
        finally:
            self.disconnect()

    def list_notes(self) -> bool:
        """List 5 most recent notes by update time.

        Returns:
            bool: True if listing successful, False otherwise
        """
        if not self.connect():
            return False

        try:
            def get_notes(session):
                # Get notes using query-service
                select_query = """
                    SELECT id, title, updated_at
                    FROM notes
                    ORDER BY updated_at DESC
                    LIMIT 5;
                """
                
                result = session.transaction().execute(select_query, commit_tx=True)
                # result is an iterator, convert to list
                result_sets = list(result)
                return result_sets[0].rows

            notes = self.query_session_pool.retry_operation_sync(get_notes)

            if not notes:
                print("📝 No notes found")
                return True

            print("📋 Recent notes:")
            print("-" * 70)
            for note in notes:
                note_id = note.id
                title = note.title
                updated_at = note.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                print(f"🗒️  {note_id} | {title[:40]:<40} | {updated_at}")

            print("-" * 70)
            print(f"📊 Total: {len(notes)} note(s)")
            return True

        except Exception as e:
            print(f"❌ Failed to list notes: {e}")
            return False
        finally:
            self.disconnect()

    def show_note(self, note_id: str) -> bool:
        """Show note content by ID.

        Args:
            note_id: Note ID

        Returns:
            bool: True if note shown successfully, False otherwise
        """
        if not self.connect():
            return False

        try:
            def get_note(session):
                # Get note using query-service
                select_query = """
                    SELECT id, title, content, created_at, updated_at
                    FROM notes
                    WHERE id = $id;
                """
                
                parameters = {'$id': ydb.TypedValue(note_id, ydb.PrimitiveType.Utf8)}
                result = session.transaction().execute(select_query, parameters, commit_tx=True)
                result_sets = list(result)
                return result_sets[0].rows

            notes = self.query_session_pool.retry_operation_sync(get_note)

            if not notes:
                print(f"❌ Note with ID '{note_id}' not found")
                return False

            note = notes[0]
            created_at = note.created_at.strftime("%Y-%m-%d %H:%M:%S")
            updated_at = note.updated_at.strftime("%Y-%m-%d %H:%M:%S")

            print("=" * 70)
            print(f"📝 Note: {note.title}")
            print("=" * 70)
            print(f"🆔 ID: {note.id}")
            print(f"📅 Created: {created_at}")
            print(f"🔄 Updated: {updated_at}")
            print("-" * 70)
            print(note.content)
            print("=" * 70)
            return True

        except Exception as e:
            print(f"❌ Failed to show note: {e}")
            return False
        finally:
            self.disconnect()

    def delete_note(self, note_id: str) -> bool:
        """Delete note by ID.

        Args:
            note_id: Note ID

        Returns:
            bool: True if note deleted successfully, False otherwise
        """
        if not self.connect():
            return False

        try:
            def delete_note(session):
                # First check if note exists
                check_query = "SELECT id FROM notes WHERE id = $id;"
                check_params = {'$id': ydb.TypedValue(note_id, ydb.PrimitiveType.Utf8)}
                
                check_result = session.transaction().execute(check_query, check_params, commit_tx=True)
                check_result_sets = list(check_result)
                existing_notes = check_result_sets[0].rows

                if not existing_notes:
                    return False

                # Delete the note using query-service
                delete_query = "DELETE FROM notes WHERE id = $id;"
                delete_params = {'$id': ydb.TypedValue(note_id, ydb.PrimitiveType.Utf8)}
                
                session.transaction().execute(delete_query, delete_params, commit_tx=True)
                return True

            deleted = self.query_session_pool.retry_operation_sync(delete_note)
            
            if not deleted:
                print(f"❌ Note with ID '{note_id}' not found")
                return False
            print(f"✅ Note '{note_id}' deleted successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to delete note: {e}")
            return False
        finally:
            self.disconnect()


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Simple CLI Notes Application with YDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s init                           # Initialize database
    %(prog)s add "Shopping List" "Milk, Eggs"  # Create note
    %(prog)s list                           # Show recent notes
    %(prog)s show abc123def                 # Show specific note
    %(prog)s delete abc123def               # Delete note
    %(prog)s --auth=env init                # Initialize with env auth

Environment Variables:
    YDB_ENDPOINT    YDB endpoint (default: grpc://localhost:2136)
    YDB_DATABASE    YDB database path (default: /local)
    
    Authentication (when --auth=env is used):
    YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS, YDB_ANONYMOUS_CREDENTIALS,
    YDB_METADATA_CREDENTIALS, YDB_ACCESS_TOKEN_CREDENTIALS, etc.
    See: https://ydb.tech/docs/en/reference/ydb-sdk/auth
        """
    )
    
    # Add global authentication option
    parser.add_argument(
        '--auth',
        choices=['anonymous', 'env'],
        default='anonymous',
        help='Authentication mode: anonymous (default) or env '
             '(from environment variables). '
             'For env mode details see: '
             'https://ydb.tech/docs/en/reference/ydb-sdk/auth'
    )

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands')

    # Init command
    subparsers.add_parser('init',
                          help='Initialize database and create notes table')

    # Add command
    add_parser = subparsers.add_parser('add', help='Create a new note')
    add_parser.add_argument('title', help='Note title')
    add_parser.add_argument('content', help='Note content')

    # List command
    subparsers.add_parser('list', help='Show 5 most recent notes')

    # Show command
    show_parser = subparsers.add_parser('show',
                                        help='Show note content by ID')
    show_parser.add_argument('id', help='Note ID')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete note by ID')
    delete_parser.add_argument('id', help='Note ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Create notes app instance with authentication mode
    use_env_auth = (args.auth == 'env')
    app = NotesApp(use_env_auth=use_env_auth)

    # Execute command
    success = False

    if args.command == 'init':
        success = app.init_database()
    elif args.command == 'add':
        success = app.add_note(args.title, args.content)
    elif args.command == 'list':
        success = app.list_notes()
    elif args.command == 'show':
        success = app.show_note(args.id)
    elif args.command == 'delete':
        success = app.delete_note(args.id)
    else:
        print(f"❌ Unknown command: {args.command}")
        parser.print_help()
        return 1

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())