from __future__ import annotations

from src.core.settings import settings
from src.core.container import build_container
from src.core.app_factory import create_app

container = build_container(settings)
app = create_app(container)

