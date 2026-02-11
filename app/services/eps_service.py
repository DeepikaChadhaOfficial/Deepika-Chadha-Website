"""
EPS API Service Layer
"""
import httpx
import logging
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger("eps-proxy")


class EPSService:
    """Service for interacting with EPS API"""
    
    def __init__(self):
        self.base_url = settings.EPS_BASE_URL
        self.timeout = settings.REQUEST_TIMEOUT
    
    async def get_tracking(self, awb: str) -> dict:
        """
        Get tracking information for an AWB number
        
        Args:
            awb: Air Waybill number
            
        Returns:
            dict: Tracking data from EPS API
            
        Raises:
            HTTPException: If tracking fails or is not found
        """
        params = {
            "Token": settings.TOKEN,
            "UserID": settings.USER_ID,
            "Password": settings.PASSWORD,
            "AwbNo": awb,
            "Type": "json",
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
            
            logger.info(f"EPS responded {response.status_code} for AWB={awb}")
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("TrackDetail"):
                logger.warning(f"No tracking found for AWB={awb}")
                raise HTTPException(status_code=404, detail="Tracking not found")
            
            return data
        
        except httpx.TimeoutException:
            logger.error(f"Timeout calling EPS for AWB={awb}")
            raise HTTPException(status_code=504, detail="EPS timeout")
        
        except httpx.HTTPStatusError as e:
            logger.error(f"EPS HTTP error status={e.response.status_code} AWB={awb}")
            raise HTTPException(status_code=502, detail="EPS service error")
        
        except HTTPException:
            raise
        
        except Exception as e:
            logger.exception(f"Unexpected error calling EPS for AWB={awb}")
            raise HTTPException(status_code=500, detail="Internal server error")
