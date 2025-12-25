from typing import Optional, Literal, Annotated
from pydantic import Field
import json

from fastmcp import FastMCP

from utils import (
    get_fhir_client,
)

## MCP Setup

mcp = FastMCP("fhir-provider-directory")

## Tools

@mcp.tool()
async def search_practitioner(
    identifier: Annotated[Optional[str], Field(description="The identifier of the practitioner; i.e. NPI")] = None,
    family: Annotated[Optional[str], Field(description="The family name (surname)")] = None,
    given: Annotated[Optional[str], Field(description="The given name (first name)")] = None,
    address_state: Annotated[Optional[str], Field(description="The state of the practitioner's address")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 25,
) -> str:
    """
    Search for Practitioners.
    
    Practitioner covers all individuals who are engaged in the healthcare process and healthcare-related services as part of their formal responsibilities
    and this Resource is used for attribution of activities and responsibilities to these individuals.
    """
    client = get_fhir_client()
    search_query = client.resources("Practitioner").limit(limit)
    
    if identifier:
        search_query = search_query.search(identifier=identifier)
    if family:
        search_query = search_query.search(family=family)
    if given:
        search_query = search_query.search(given=given)
    if address_state:
        search_query = search_query.search(address_state=address_state)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_practitioner_role(
    practitioner: Annotated[Optional[str], Field(description='reference to the practitioner (e.g. "Practitioner/123" or just "123")')] = None,
    organization: Annotated[Optional[str], Field(description="reference to the organization")] = None,
    location: Annotated[Optional[str], Field(description="reference to the location")] = None,
    specialty: Annotated[Optional[str], Field(description="Code for specialty")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 100,
) -> str:
    """Search for PractitionerRoles.
    
    The PractitionerRole describes the types of services that practitioners provide for an organization at specific location(s).
    
    The PractitionerRole resource can be used in multiple contexts including:
    - Provider Registries where it indicates what a practitioner can perform for an organization (may indicate multiple healthcareservices, locations, and roles)
    - In a Clinical system where it indicates the role, healthcareservice and location details associated with a practitioner that are applicable to the healthcare event (e.g. Observation, Appointment, Condition, CarePlan)
    - In a Clinical system as a point of reference rather than an event, such as a patient's preferred general practitioner (at a specific clinic)
    """
    client = get_fhir_client()
    search_query = client.resources("PractitionerRole").limit(limit)
    
    if practitioner:
        search_query = search_query.search(practitioner=practitioner)
    if organization:
        search_query = search_query.search(organization=organization)
    if location:
        search_query = search_query.search(location=location)
    if specialty:
        search_query = search_query.search(specialty=specialty)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_location(
    name: Annotated[Optional[str], Field(description="A portion of the location's name or alias")] = None,
    address: Annotated[Optional[str], Field(description="A portion of the address parts")] = None,
    city: Annotated[Optional[str], Field(description="The city specified in an address")] = None,
    state: Annotated[Optional[str], Field(description="The state specified in an address")] = None,
    postal_code: Annotated[Optional[str], Field(description="A postal code specified in an address")] = None,
    usage: Annotated[Optional[str], Field(description="Location usage code")] = None,
    status: Annotated[Optional[str], Field(description="active | suspended | inactive")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 50,
) -> str:
    """
    Search for Locations.
    
    A Location includes both incidental locations (a place which is used for healthcare without prior designation or authorization) and dedicated,
    formally appointed locations. Locations may be private, public, mobile or fixed and scale from small freezers to full hospital buildings or parking garages.

    Examples of Locations are:
    - Building, ward, corridor, room or bed
    - Mobile Clinic
    - Freezer, incubator
    - Vehicle or lift
    - Home, shed, or a garage
    - Road, parking place, a park
    - Ambulance (generic)
    - Ambulance (specific)
    - Patient's Home (generic)
    - Jurisdiction
    """
    client = get_fhir_client()
    search_query = client.resources("Location").limit(limit)
    
    if name:
        search_query = search_query.search(name=name)
    if address:
        search_query = search_query.search(address=address)
    if city:
        search_query = search_query.search(address_city=city)
    if state:
        search_query = search_query.search(address_state=state)
    if postal_code:
        search_query = search_query.search(address_postalcode=postal_code)
    if status:
        search_query = search_query.search(status=status)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_organization(
    name: Annotated[Optional[str], Field(description="A portion of the organization's name")] = None,
    type: Annotated[Optional[str], Field(description="A code for the type of organization (e.g., prov | dept | ins | pay)")] = None,
    partof: Annotated[Optional[str], Field(description="Reference to the parent organization")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 25,
) -> str:
    """
    Search for Organizations.
    
    This resource may be used in a shared registry of contact and other information for various organizations or it can be used merely as a support for 
    other resources that need to reference organizations, perhaps as a document, message or as a contained resource. If using a registry approach, it's 
    entirely possible for multiple registries to exist, each dealing with different types or levels of organization.
    """
    client = get_fhir_client()
    search_query = client.resources("Organization").limit(limit)
    
    if name:
        search_query = search_query.search(name=name)
    if type:
        search_query = search_query.search(type=type)
    if partof:
        search_query = search_query.search(partof=partof)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_organization_affiliation(
    primary_organization: Annotated[Optional[str], Field(description="Reference to the primary organization")] = None,
    participating_organization: Annotated[Optional[str], Field(description="Reference to the participating organization")] = None,
    role: Annotated[Optional[str], Field(description="Definition of the role the participatingOrganization plays")] = None,
    specialty: Annotated[Optional[str], Field(description="Specific specialty of the participatingOrganization in the context of the role")] = None,
    location: Annotated[Optional[str], Field(description="The location(s) at which the role occurs")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 100,
) -> str:
    """
    Search for OrganizationAffiliations.

    A relationship between 2 organizations over a period of time, where the entities are separate business entities. The relationship can optionally include details of locations/services from the participating organization.

    The OrganizationAffiliation enables defining non-hierarchical relationships between organizations. For example:
    - One organization may provide services to another organization (e.g. An agency service providing casual staff, a radiology service, a diagnostic lab, catering services, community care services etc.)
    - Two or more organizations may form a partnership or joint venture
    - An organization may be a member of an association, but not owned by it (e.g. a hospital is a member the American Hospital Association, a hospital is a member of a health information exchange network)
    - Spotless Cleaning Services (participatingOrganization) is a supplier (code) to General Hospital (organization)
    - General Hospital (participatingOrganization) is a member (code) of Eastern HIE (organization)
    """
    client = get_fhir_client()
    search_query = client.resources("OrganizationAffiliation").limit(limit)
    
    if primary_organization:
        search_query = search_query.search(primary_organization=primary_organization)
    if participating_organization:
        search_query = search_query.search(participating_organization=participating_organization)
    if role:
        search_query = search_query.search(role=role)
    if specialty:
        search_query = search_query.search(specialty=specialty)
    if location:
        search_query = search_query.search(location=location)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_healthcare_service(
    organization: Annotated[Optional[str], Field(description="The organization that provides this Healthcare Service")] = None,
    location: Annotated[Optional[str], Field(description="The location(s) where this Healthcare Service is provided")] = None,
    name: Annotated[Optional[str], Field(description="A portion of the Healthcare Service name")] = None,
    category: Annotated[Optional[str], Field(description="Service Category of the Healthcare Service")] = None,
    type: Annotated[Optional[str], Field(description="The Code or Name of the Service Type of the Healthcare Service")] = None,
    specialty: Annotated[Optional[str], Field(description="The specialty of the service provided")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 25,
) -> str:
    """
    
    Search for HealthcareServices.

    The HealthcareService resource is used to describe a single healthcare service or category of services that are provided by an organization at a location.
    The location of the services could be virtual, as with telemedicine services.

    Common examples of HealthcareServices resources are:
    - Allied Health
    - Clinical Neuropsychologist
    - Podiatry Service
    - Smallville Hospital Emergency Services
    - Respite care provided at a nursing home or hostel
    - 24hr crisis telephone counseling service
    - Information, advice and/or referral services; Disability, Telecommunications
    - Rural TeleHealth Services
    - Hospital in the home
    - Yellow Cabs
    - Pharmacy
    - Active Rehab
    - Social Support
    - Drug and/or alcohol counseling
    - Day Programs, Adult Training & Support Services
    - Consulting psychologists and/or psychology services
    - Group Hydrotherapy
    - Little River Home Maintenance
    - CT Head Scan w/o Contrast
    - CT Head Scan with Contrast
    - CT Head+Chest Scan with Contrast
    """
    client = get_fhir_client()
    search_query = client.resources("HealthcareService").limit(limit)
    
    if organization:
        search_query = search_query.search(organization=organization)
    if location:
        search_query = search_query.search(location=location)
    if name:
        search_query = search_query.search(name=name)
    if category:
        search_query = search_query.search(service_category=category)
    if type:
        search_query = search_query.search(service_type=type)
    if specialty:
        search_query = search_query.search(specialty=specialty)
        
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def search_insurance_plan(
    name: Annotated[Optional[str], Field(description="A portion of the insurance plan name")] = None,
    type: Annotated[Optional[str], Field(description="Kind of plan (e.g. medical | dental | mental)")] = None,
    administered_by: Annotated[Optional[str], Field(description="Product administrator (Organization)")] = None,
    owned_by: Annotated[Optional[str], Field(description="Product issuer (Organization)")] = None,
    coverage_area: Annotated[Optional[str], Field(description="The coverage area for the product (Location)")] = None,
    limit: Annotated[Optional[int], Field(description="Number of results to return", ge=1, le=1000)] = 25,
) -> str:
    """
    Search for InsurancePlans.
    
    A product is a discrete package of health insurance coverage benefits that are offered under a particular network type. A given payer's products 
    typically differ by network type and/or coverage benefits. A plan pairs the health insurance coverage benefits under a product with the particular 
    cost sharing structure offered to a consumer. A given product may comprise multiple plans.
    
    InsurancePlan describes a health insurance offering comprised of a list of covered benefits (i.e. the product), costs associated with those benefits 
    (i.e. the plan), and additional information about the offering, such as who it is owned and administered by, a coverage area, contact information, etc.
    """
    client = get_fhir_client()
    search_query = client.resources("InsurancePlan").limit(limit)
    
    if name:
        search_query = search_query.search(name=name)
    if type:
        search_query = search_query.search(type=type)
    if administered_by:
        search_query = search_query.search(administered_by=administered_by)
    if owned_by:
        search_query = search_query.search(owned_by=owned_by)
    if coverage_area:
        search_query = search_query.search(coverage_area=coverage_area)
    
    results = await search_query.fetch_all()
    return json.dumps([r.serialize() for r in results])


@mcp.tool()
async def read_resource(
    resource_type: Annotated[Literal["Practitioner", "PractitionerRole", "Organization", "Location", "HealthcareService", "InsurancePlan", "OrganizationAffiliation"], Field(description='The type of resource (e.g., "Practitioner", "Organization", "Location")')],
    id: Annotated[str, Field(description="The logical ID of the resource")]
) -> str:
    """Read a specific FHIR resource by type and ID."""
    client = get_fhir_client()
    resource = await client.resources(resource_type).get(id=id)
    
    return resource.serialize()

## Server

if __name__ == "__main__":
    mcp.run()
