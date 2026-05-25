from dataclasses import dataclass


EDU_SERVICE = "EDU_SERVICE"
VKS_SERVICE = "VKS_SERVICE"
MOUNT_SERVICE = "MOUNT_SERVICE"
MODPC_SERVICE = "MODPC_SERVICE"
REGWORKS_SERVICE = "REGWORKS_SERVICE"
IU_SERVICE = "IU_SERVICE"


@dataclass(frozen=True)
class ITSMServiceMapping:
    service: str
    service_2nd_level: str = ""
    service_3rd_level: str = ""
    service_4th_level: str = ""
    basic_service: str = ""


DEFAULT_SERVICE_MAPPING = ITSMServiceMapping(
    service="174291345197423243",
    service_2nd_level="173979049797789044",
    service_3rd_level="174288904894201605",
    basic_service=(
        "Сопровождение мероприятий и учебного процесса. "
        "Сопровождение учебного процесса. "
        "Сопровождение учебного процесса."
    ),
)


SERVICE_MAPPINGS: dict[str, ITSMServiceMapping] = {
    EDU_SERVICE: DEFAULT_SERVICE_MAPPING,
    VKS_SERVICE: DEFAULT_SERVICE_MAPPING,
    MOUNT_SERVICE: DEFAULT_SERVICE_MAPPING,
    MODPC_SERVICE: DEFAULT_SERVICE_MAPPING,
    REGWORKS_SERVICE: DEFAULT_SERVICE_MAPPING,
    IU_SERVICE: DEFAULT_SERVICE_MAPPING,
}


def get_itsm_service_mapping(service_code: str) -> ITSMServiceMapping:
    return SERVICE_MAPPINGS.get(service_code, DEFAULT_SERVICE_MAPPING)
