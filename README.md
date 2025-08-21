# Simple CLI Notes Application with YDB

A simple command-line notes application that uses YDB (Yandex Database) as storage. Perfect for learning YDB basics and building simple CLI tools.

## Quick Start (Docker Compose)

The fastest way to get started (no Python installation required):

```bash
# Clone and navigate to the project
git clone <repository-url>
cd ydb-mcp-show

# Start YDB database
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Initialize the database
docker-compose run --rm notes-app init

# Create your first note
docker-compose run --rm notes-app add "Hello" "My first note with YDB!"

# List notes
docker-compose run --rm notes-app list

# View YDB Web UI at http://localhost:8765
# (Use docker-compose ps to confirm "healthy" status for reliable DB readiness)
```

## Features

- 📝 Create new notes with title and content
- 📋 List 5 most recent notes by update time
- 👀 View full note content by ID
- 🗑️ Delete notes by ID
- 🚀 Initialize database with a single command
- 🐳 Docker support for easy deployment

## Quick Start

### Prerequisites

- Docker and Docker Compose (no Python installation required!)

### Installation

1. Clone or download the project:
```bash
git clone <repository-url>
cd ydb-mcp-show
```

2. **Using Docker Compose (Recommended - No Local Python Required)**
```bash
# Start YDB database
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Build and run the notes application
docker-compose build notes-app
```

3. **Option B: Local Python with Docker YDB**
```bash
# Start YDB database only
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Install Python dependencies locally
pip install -r requirements.txt
```

4. **Option C: Using external YDB instance**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables for external YDB
export YDB_ENDPOINT="grpc://your-ydb-host:2136"
export YDB_DATABASE="/your/database/path"
```

### Usage with Docker Compose (Recommended)

1. **Start YDB and initialize the database** (first time only):
```bash
# Start YDB database
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Initialize the database
docker-compose run --rm notes-app init
```

2. **Create a new note**:
```bash
docker-compose run --rm notes-app add "Shopping List" "Milk, Bread, Eggs, Apples"
```

3. **List recent notes**:
```bash
docker-compose run --rm notes-app list
```

4. **View a specific note**:
```bash
docker-compose run --rm notes-app show abc123def-456-789
```

5. **Delete a note**:
```bash
docker-compose run --rm notes-app delete abc123def-456-789
```

6. **Access YDB Web UI**:
   - Open http://localhost:8765 in your browser
   - Explore your database, tables, and data

7. **Stop YDB when done**:
```bash
docker-compose down
```

### Usage with Local Python (Alternative)

If you prefer to run Python locally with Docker YDB:

1. **Start YDB and initialize the database** (first time only):
```bash
# Start YDB database
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Initialize the database
python notes.py init
```

2. **Use the application locally**:
```bash
python notes.py add "Shopping List" "Milk, Bread, Eggs, Apples"
python notes.py list
python notes.py show abc123def-456-789
python notes.py delete abc123def-456-789
```

> **💡 Clean Test Environment:** Data is not persisted between container restarts for easy cleanup. To reset everything, just run `docker-compose restart ydb`.

### Authentication

By default, the application uses anonymous authentication (suitable for local development). For production use with authentication, use the `--auth=env` option:

```bash
# Use authentication from environment variables
python notes.py --auth=env init
python notes.py --auth=env list
```

For details about authentication environment variables, see: https://ydb.tech/docs/en/reference/ydb-sdk/auth

## Complete Example

Here's a complete example of getting started with the notes application using Docker Compose:

```bash
# 1. Start YDB database
docker-compose up -d ydb

# 2. Wait for YDB to be ready (check until status shows "healthy")
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# 3. Initialize the database
docker-compose run --rm notes-app init

# 4. Create some notes
docker-compose run --rm notes-app add "Shopping List" "Milk, Bread, Eggs, Coffee"
docker-compose run --rm notes-app add "Meeting Notes" "Discuss Q4 planning and budget allocation"
docker-compose run --rm notes-app add "Ideas" "New feature: note categories and tags"

# 5. List all notes
docker-compose run --rm notes-app list

# 6. View a specific note (use ID from the list)
docker-compose run --rm notes-app show <note-id>

# 7. Clean up
docker-compose down
```

**Alternative with local Python:**

```bash
# 1. Start YDB database
docker-compose up -d ydb

# 2. Wait for YDB to be ready (check until status shows "healthy")
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# 3. Install dependencies
pip install -r requirements.txt

# 3. Initialize and use the application
python notes.py init
python notes.py add "Shopping List" "Milk, Bread, Eggs, Coffee"
python notes.py list
python notes.py show <note-id>

# 4. Clean up
docker-compose down
```

> **💡 Note:** Database content is ephemeral - it doesn't persist between container restarts. This is by design for easy testing and cleanup. To get a fresh database, simply restart the container with `docker-compose restart ydb`.

## Local Development with Docker Compose (Recommended)

The easiest way to get started is using Docker Compose - no local Python installation required:

```bash
# Start YDB database
docker-compose up -d ydb

# Wait for YDB to be ready (usually takes 10-30 seconds)
docker-compose ps
# Wait until ydb-local container shows "Up X minutes (healthy)" status
# Note: Web UI at http://localhost:8765 may load before DB is ready for queries

# Initialize and use the application
docker-compose run --rm notes-app init
docker-compose run --rm notes-app add "My First Note" "Hello YDB!"
docker-compose run --rm notes-app list

# Access Web UI at http://localhost:8765
# (docker-compose ps shows more reliable "healthy" status for DB readiness)

# Stop when done
docker-compose down
```

**Note:** The database content is not persisted between container restarts. This is intentional for easy cleanup of the test environment - simply restart the container to get a fresh database.

## CLI Application in Docker

### Using Docker Compose (Recommended)

The recommended approach is to use `docker-compose run` which automatically handles networking:

```bash
# Build the application (first time only)
docker-compose build notes-app

# Use the application
docker-compose run --rm notes-app init
docker-compose run --rm notes-app add "Title" "Content"
docker-compose run --rm notes-app list
```

### Manual Docker Build

You can also build and run the application manually:

```bash
# Build the CLI application image
docker build -t ydb-notes .

# If using docker-compose YDB, connect to it
docker run --rm --network ydb-mcp-show_default ydb-notes init

# Or with external YDB
docker run --rm \
  -e YDB_ENDPOINT="grpc://your-ydb-host:2136" \
  -e YDB_DATABASE="/your/database/path" \
  ydb-notes init
```

### Docker CLI with Authentication

```bash
# With docker-compose (anonymous authentication - default)
docker-compose run --rm notes-app init

# With docker-compose using environment authentication
docker-compose run --rm \
  -e YDB_ACCESS_TOKEN_CREDENTIALS="your-token" \
  notes-app --auth=env init

# Manual docker run with anonymous authentication (default)
docker run --rm \
  -e YDB_ENDPOINT="grpc://your-ydb-host:2136" \
  -e YDB_DATABASE="/your/database/path" \
  ydb-notes init

# Manual docker run with environment-based authentication
docker run --rm \
  -e YDB_ENDPOINT="grpc://your-ydb-host:2136" \
  -e YDB_DATABASE="/your/database/path" \
  -e YDB_ACCESS_TOKEN_CREDENTIALS="your-token" \
  ydb-notes --auth=env init
```

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize database and create notes table | `python notes.py init` |
| `add <title> <content>` | Create a new note | `python notes.py add "Title" "Content"` |
| `list` | Show 5 most recent notes | `python notes.py list` |
| `show <id>` | Display note content by ID | `python notes.py show abc123...` |
| `delete <id>` | Remove note by ID | `python notes.py delete abc123...` |

### Global Options

| Option | Description | Example |
|--------|-------------|---------|
| `--auth=anonymous` | Use anonymous authentication (default) | `python notes.py --auth=anonymous init` |
| `--auth=env` | Use authentication from environment variables | `python notes.py --auth=env init` |

## Configuration

The application uses environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `YDB_ENDPOINT` | `grpc://localhost:2136` | YDB gRPC endpoint |
| `YDB_DATABASE` | `/local` | YDB database path |

### Authentication Environment Variables (when using `--auth=env`)

When using `--auth=env`, the application automatically detects authentication method from environment variables. For complete list of supported authentication variables, see: https://ydb.tech/docs/en/reference/ydb-sdk/auth

Common authentication variables:
- `YDB_ACCESS_TOKEN_CREDENTIALS` - Access token for authentication
- `YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS` - Path to service account key file
- `YDB_ANONYMOUS_CREDENTIALS=1` - Force anonymous authentication
- `YDB_METADATA_CREDENTIALS=1` - Use metadata service authentication

## Database Schema

The application creates a single table called `notes`:

```sql
CREATE TABLE notes (
    id Utf8,                -- Unique note ID (UUID)
    title Utf8,             -- Note title
    content Utf8,           -- Note content
    created_at Timestamp,   -- Creation timestamp
    updated_at Timestamp,   -- Last update timestamp
    PRIMARY KEY (id)
);
```

## Development

### Project Structure

```
.
├── notes.py              # Main application file
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Local YDB setup
├── Dockerfile           # CLI app Docker configuration
├── README.md            # This file
└── LICENSE              # MIT license
```

### Contributing

This is a simple example project. Feel free to:
- Add new features (search, categories, etc.)
- Improve error handling
- Add tests
- Enhance the CLI interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Learn More

- [YDB Documentation](https://ydb.tech/en/docs/)
- [YDB Python SDK](https://github.com/ydb-platform/ydb-python-sdk)
- [YDB Docker Images](https://hub.docker.com/r/ydbplatform/ydb)

## Support

This is an educational example project. For YDB-specific questions, please refer to the official YDB documentation and community resources.
