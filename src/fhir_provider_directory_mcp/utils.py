import os
from fhirpy import AsyncFHIRClient

def get_fhir_client() -> AsyncFHIRClient:
    """Returns an AsyncFHIRClient; defaults to UHC unless environment variable FHIR_SERVER_URL is set."""
    base_url = os.getenv("FHIR_SERVER_URL", "https://flex.optum.com/fhirpublic/R4")
    return AsyncFHIRClient(url=base_url, aiohttp_config={"ssl": False})