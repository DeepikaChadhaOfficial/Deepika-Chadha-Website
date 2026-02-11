"""
Tracking API routes
"""
from fastapi import APIRouter, HTTPException
import logging

from app.services.eps_service import EPSService

router = APIRouter()
logger = logging.getLogger("eps-proxy")
eps_service = EPSService()


@router.get("/{awb}")
async def get_tracking(awb: str):
    """
    Get tracking information for an AWB number
    
    Args:
        awb: Air Waybill number to track
        
    Returns:
        Tracking details from EPS API
    """
    logger.info(f"Tracking request for AWB={awb}")
    
    try:
        data = await eps_service.get_tracking(awb)
        return data
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error for AWB={awb}")
        raise HTTPException(status_code=500, detail="Internal server error")
