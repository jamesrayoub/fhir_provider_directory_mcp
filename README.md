# FHIR Provider Directory MCP Server

A Model Context Protocol (MCP) server that exposes a FHIR-based Provider Directory. This server is designed to work with standard FHIR R4 APIs, specifically configured for the UHC Public API but adaptable to others.

## Features

- **FHIR R4 Compliant**: Interacts with standard FHIR resources.
- **Provider Directory Focus**: Specialized tools for searching practitioners, organizations, locations, and insurance plans.
- **FastMCP**: Built on the efficient `fastmcp` framework.
- **Type-Safe Parameters**: Uses Pydantic's `Annotated` and `Field` for parameter validation and documentation.

## Setup

### Prerequisites

- Python 3.13+
- `uv` (recommended) or `pip`

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   uv sync
   ```

### Configuration

The server uses environment variables for configuration. Default values are provided, but you can override them by creating a `.env` file in the root directory:

```env
FHIR_SERVER_URL=https://flex.optum.com/fhirpublic/R4
```

## Tools Available

### `search_practitioner`
Search for Practitioners in the directory.
- **Args**:
  - `identifier`: The identifier of the practitioner (e.g., NPI).
  - `family`: The family name (surname).
  - `given`: The given name (first name).
  - `address_state`: The state of the practitioner's address.
  - `limit`: Number of results to return (1-1000, default: 25).

### `search_practitioner_role`
Search for roles that practitioners play within an organization at a location.
- **Args**:
  - `practitioner`: Reference to the practitioner (e.g., "Practitioner/123" or just "123").
  - `organization`: Reference to the organization.
  - `location`: Reference to the location.
  - `specialty`: Code for the specialty.
  - `limit`: Number of results to return (1-1000, default: 100).

### `search_location`
Search for physical locations (e.g., clinics, hospitals).
- **Args**:
  - `name`: A portion of the location's name or alias.
  - `address`: A portion of the address parts.
  - `city`: The city specified in an address.
  - `state`: The state specified in an address.
  - `postal_code`: A postal code specified in an address.
  - `usage`: Location usage code.
  - `status`: Location status (`active`, `suspended`, or `inactive`).
  - `limit`: Number of results to return (1-1000, default: 50).

### `search_organization`
Search for organizations (e.g., hospitals, insurance companies).
- **Args**:
  - `name`: A portion of the organization's name.
  - `type`: A code for the type of organization (e.g., `prov`, `dept`, `ins`, `pay`).
  - `partof`: Reference to the parent organization.
  - `limit`: Number of results to return (1-1000, default: 25).

### `search_organization_affiliation`
Search for relationships between organizations.
- **Args**:
  - `primary_organization`: Reference to the primary organization.
  - `participating_organization`: Reference to the participating organization.
  - `role`: Definition of the role the participatingOrganization plays.
  - `specialty`: Specific specialty of the participatingOrganization in the context of the role.
  - `location`: The location(s) at which the role occurs.
  - `limit`: Number of results to return (1-1000, default: 100).

### `search_healthcare_service`
Search for specific services provided by an organization at a location.
- **Args**:
  - `organization`: The organization that provides this Healthcare Service.
  - `location`: The location(s) where this Healthcare Service is provided.
  - `name`: A portion of the Healthcare Service name.
  - `category`: Service Category of the Healthcare Service.
  - `type`: The Code or Name of the Service Type of the Healthcare Service.
  - `specialty`: The specialty of the service provided.
  - `limit`: Number of results to return (1-1000, default: 25).

### `search_insurance_plan`
Search for insurance products.
- **Args**:
  - `name`: A portion of the insurance plan name.
  - `type`: Kind of plan (e.g., `medical`, `dental`, `mental`).
  - `administered_by`: Product administrator (Organization).
  - `owned_by`: Product issuer (Organization).
  - `coverage_area`: The coverage area for the product (Location).
  - `limit`: Number of results to return (1-1000, default: 25).

### `read_resource`
Read a specific FHIR resource by type and ID.
- **Args**:
  - `resource_type`: The type of resource (e.g., `Practitioner`, `Organization`, `Location`, `HealthcareService`, `InsurancePlan`, `PractitionerRole`, `OrganizationAffiliation`).
  - `id`: The logical ID of the resource.

## Development

Run the server locally for dev/testing:

```bash
uv run src/fhir_provider_directory_mcp/server.py
```

## Usage with MCP Clients

To use this server with an MCP client (like Claude Desktop), add the following configuration to your `mcp_config.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fhir-provider-directory": {
      "command": "uv",
      "args": [
        "run",
        "src/fhir_provider_directory_mcp/server.py"
      ],
      "env": {
        "FHIR_SERVER_URL": "https://flex.optum.com/fhirpublic/R4"
      }
    }
  }
}
```

**Note**: You may need to provide the absolute path to `src/fhir_provider_directory_mcp/server.py` and `uv` if the client runs from a different directory. For example:

```json
{
  "mcpServers": {
    "fhir-provider-directory": {
      "command": "/path/to/uv",
      "args": [
        "run",
        "/absolute/path/to/fhir-provider-directory-mcp/src/fhir_provider_directory_mcp/server.py"
      ],
      "env": {
        "FHIR_SERVER_URL": "https://flex.optum.com/fhirpublic/R4"
      }
    }
  }
}
```

