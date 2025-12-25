# FHIR Provider Directory MCP Server

A Model Context Protocol (MCP) server that exposes a FHIR-based Provider Directory. This server is designed to work with standard FHIR R4 APIs, specifically configured for the UHC Public API but adaptable to others.

## Features

- **FHIR R4 Compliant**: Interacts with standard FHIR resources.
- **Provider Directory Focus**: specialized tools for searching practitioners, organizations, locations, and insurance plans.
- **Pydantic Validation**: Uses `fhir.resources` to validate responses, ensuring data integrity while being resilient to non-fatal errors.
- **FastMCP**: Built on the efficient `fastmcp` framework.

## Setup

### Prerequisites

- Python 3.10+
- `uv` (recommended) or `pip`

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   uv sync
   ```
   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root directory (optional, defaults provided):

```env
FHIR_BASE_URL=https://flex.optum.com/fhirpublic/R4/
LOG_LEVEL=INFO
```

## Tools Available

### `search_practitioner`
Search for Practitioners in the directory.
- **Args**:
  - `name`: A portion of the family or given name.
  - `family`: The family name (surname).
  - `given`: The given name (first name).
  - `id`: The logical ID of the practitioner.

### `get_practitioner`
Retrieve a specific Practitioner by their logical ID.
- **Args**:
  - `id`: The logical ID of the practitioner.

### `search_practitioner_role`
Search for roles that practitioners play within an organization at a location.
- **Args**:
  - `practitioner`: Reference to the practitioner (e.g., "Practitioner/123").
  - `organization`: Reference to the organization.
  - `location`: Reference to the location.
  - `specialty`: Code for the specialty.

### `search_location`
Search for physical locations (e.g., clinics, hospitals).
- **Args**:
  - `name`: A portion of the location's name or alias.
  - `address`: A portion of the address parts.
  - `city`: The city.
  - `state`: The state.
  - `postalCode`: The postal code.
  - `usage`: Location usage code.
  - `status`: One of `active`, `suspended`, `inactive`.

### `search_organization`
Search for organizations (e.g., hospitals, insurance companies).
- **Args**:
  - `name`: A portion of the organization's name.
  - `type`: Code for the type of organization (e.g., `prov`, `dept`, `ins`, `pay`).
  - `partof`: Reference to the parent organization.

### `search_organization_affiliation`
Search for relationships between organizations.
- **Args**:
  - `primary_organization`: Reference to the primary organization.
  - `participating_organization`: Reference to the participating organization.
  - `role`: Definition of the role.
  - `specialty`: Specific specialty in the context of the role.
  - `location`: Location at which the role occurs.

### `search_healthcare_service`
Search for specific services provided by an organization at a location.
- **Args**:
  - `organization`: The providing organization.
  - `location`: The location where service is provided.
  - `name`: A portion of the service name.
  - `category`: Service Category code.
  - `type`: Service Type code.
  - `specialty`: Specialty code.

### `search_insurance_plan`
Search for insurance products.
- **Args**:
  - `name`: A portion of the plan name.
  - `type`: Kind of plan (e.g., `medical`, `dental`).
  - `administered_by`: Product administrator reference.
  - `owned_by`: Product issuer reference.
  - `identifier`: Any identifier for the product.

## Development

Run the server locally for dev/testing:

```bash
uv run src/server.py
```

## Usage with MCP Clients

To use this server with an MCP client (like Claude Desktop), add the following configuration to your `mcp_config.json` or `claude_desktop_config.json`. Assuming you are in the project root:

```json
{
  "mcpServers": {
    "fhir-provider-directory": {
      "command": "uv",
      "args": [
        "run",
        "src/server.py"
      ],
      "env": {
        "FHIR_BASE_URL": "https://flex.optum.com/fhirpublic/R4/",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Note**: You may need to provide the absolute path to `src/server.py` and `uv` if the client runs from a different directory. For example:

```json
{
  "mcpServers": {
    "fhir-provider-directory": {
      "command": "/path/to/uv",
      "args": [
        "run",
        "/absolute/path/to/fhir-provider-directory-mcp/src/server.py"
      ],
      ...
    }
  }
}
```

