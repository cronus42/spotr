
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class AvailabilityZone:
    zone_name: str
    price_history: List[Dict[str, Any]]

    @property
    def current_price(self) -> Optional[float]:
        if self.price_history:
            return float(self.price_history[0]['SpotPrice'])
        else:
            return None

    def __repr__(self):
        price = str(self.current_price)
        zone_name = self.zone_name
        return f"{zone_name} for ${price}/hr"
