from pydantic import BaseModel, Field
from typing import List, Optional

class SavingRow(BaseModel):
    system_name: str
    savings: float
    
class Savings(BaseModel):
    system_name: str
    capacity: float
    savings: float
    rank : int = Field(gt = 0)
    
class Analysis_Json(BaseModel):  
    total_sites : int = Field(gt=0)
    total_saving_this_yr : float
    total_bill_prd_saving : float
    top_5_performer : List[Savings]
    bottom_5_performer : List[Savings]
    
class DataQuality(BaseModel):
    negative_sites: int = Field(gt=-1)
    zero_savings: int = Field(gt=-1)
    missing_capacity: int = Field(gt=-1)
    duplicate_sites: int = Field(gt=-1)
    
class PortfolioMetrics(BaseModel):
    total_sites: int
    report_period_savings: float
    operating_year_savings: float
    negative_savings_site : int
    sites_marked_healthy : int
    sites_marked_average : int
    sites_marked_needs_attention : int
    sites_marked_critical : int
    new_sites: int
    
class Metrics(BaseModel):
   capacity_kw: float
   report_period_savings: float
   operating_year_savings: float 
   
class SiteHealth(BaseModel):
    site_name: str
    score: Optional[int]
    status: str
    reasons:List[str]
    metrics: Metrics
    
class OverAllMatrix(BaseModel):
    data_quality : DataQuality
    statistical_performance : Analysis_Json
    site_wise_report : List[SiteHealth]

class SiteMarker(BaseModel):
    site_name: str
    reasons:List[str] | None = None
    savings: float | None = None

class AIContent(BaseModel):
    report_period : str
    portfolio : PortfolioMetrics
    data_quality: DataQuality
    top_performers: List[SiteMarker]
    sites_needing_attention : List[SiteMarker]
    critical_sites: List[SiteMarker]


