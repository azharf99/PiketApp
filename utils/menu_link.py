def export_menu_link(link_name:str = "") -> dict[str, str]:
    return {
    "home": "bg-lime-300" if link_name == "home" else "bg-gray-300",
    "report": "bg-lime-300" if link_name == "report" else "bg-gray-300",
    "menu": "bg-lime-300" if link_name == "menu" else "bg-gray-300",
    "profile": "bg-lime-300" if link_name == "profile" else "bg-gray-300",
}


def export_home_kwargs(link_name:str = "") -> dict[str, str]:
    home_kwargs = {"site_title": "Piket SMA IT AL BINAA"}
    home_kwargs.update(export_menu_link(link_name))
    return home_kwargs