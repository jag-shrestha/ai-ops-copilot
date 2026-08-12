import pandas as pd
import numpy as np
import structures
from pandas import DateOffset


def read_report():
    rep = pd.read_excel("data/Report 1.xlsx")
    rep = rep[6:]
    new_header = rep.iloc[0]
    rep = rep[1:]
    rep.columns = new_header
    rep.reset_index(drop = True, inplace = True)
    return rep[:191]

def statistical_analysis(report):
    savings_sorted = (report.sort_values(by='Total Savings: Current Bill Period', ascending=False).reset_index(drop=True))
    savings_sorted['rank'] = savings_sorted.index + 1
    top_5 = savings_sorted.head(5)
    bottom_5 = savings_sorted.tail(5)
    
    max_savings = report.loc[report['Total Savings: Current Operating Year'].idxmax()]
    min_savings = report.loc[report['Total Savings: Current Operating Year'].idxmin()]
    
    hla = structures.Analysis_Json(
            total_sites=len(report),
            total_saving_this_yr=report['Total Savings: Current Operating Year'].sum(),
            total_bill_prd_saving=report['Total Savings: Current Bill Period'].sum(),
            top_5_performer =  [structures.Savings(system_name = row['System Name'],
                                          capacity= row['Power (kW)'],
                                          savings = row['Total Savings: Current Bill Period'],
                                          rank = row['rank'])
                                for index, row in top_5.iterrows()],
            bottom_5_performer =  [structures.Savings(system_name = row['System Name'],
                                          capacity= row['Power (kW)'],
                                          savings = row['Total Savings: Current Bill Period'],
                                          rank = row['rank'])
                                for index, row in bottom_5.iterrows()]
        )
    return hla

def data_quality_check(report):
    dq = structures.DataQuality(
              negative_sites = len(report[report['Total Savings: Current Bill Period'] < 0]),
              zero_savings= len(report[report['Total Savings: Current Bill Period'] == 0]),
              missing_capacity = len(report[report['Power (kW)'].isna()]),
              duplicate_sites = len(report[report['System-ID'].duplicated()])
        )
    return dq
    
def apply_penalty(report, mask, penalty, reason):
    report.loc[mask, 'score'] -= penalty
    report.loc[mask, 'reason'] = (report.loc[mask, 'reason'].fillna('').apply(lambda x: f"{x},{reason}" if x else reason))
    
    
def calculate_site_health(report):
    report['score'] = 100.0
    report['reason'] = ''

    report['Power (kW)'] = pd.to_numeric(report['Power (kW)'], errors='coerce')

    avg_current_savings = report['Total Savings: Current Bill Period'].mean() * 0.25
    avg_op_yr_savings = (report['Total Savings: Current Operating Year'].mean()) * 0.5
    p75_power = report['Power (kW)'].quantile(0.75)

    # Negative savings
    mask = report['Total Savings: Current Bill Period'] < 0
    apply_penalty(report, mask, 40, "Negative Savings in this bill period")
    

    # Zero savings
    mask = report['Total Savings: Current Bill Period'] == 0
    apply_penalty(report, mask, 20, "Zero Savings in this bill period")

    # No savings
    mask = report['Total Savings: Current Bill Period'].isna()
    apply_penalty(report, mask, 25, "No savings found for this bill period")

    # Large system + lower savings
    mask = ((report['Power (kW)'] > p75_power) & (report['Total Savings: Current Bill Period'] < avg_current_savings))
    apply_penalty(report, mask, 20, "Large System and less savings for this bill period")

    # Lower operational-year savings
    mask = (report['Total Savings: Current Operating Year'] < avg_op_yr_savings)
    apply_penalty(report, mask, 10, "Lesser than Average operational year savings")

    # New sitess
    report['System Live Date'] = pd.to_datetime(report['System Live Date'], errors='coerce')
    mask = report['System Live Date'] >= (pd.Timestamp.today().normalize() - DateOffset(months=2))
    apply_penalty(report, mask, pd.NA, 'New site')

    # Ensure score stays between 0 and 100
    report['score'] = report['score'].clip(lower=0, upper=100)
    
    conditions = [report["score"].isna(),
                  report["score"] > 90,
                  report["score"] >= 60,
                  report["score"] >= 40,
                  report["score"] < 40]

    choices = ["New Site",
               "Healthy",
               "Average",
               "Need Attention",
               "Critical"]
    
    report["status"] = np.select(conditions, choices, default="New Site")
    
    site_health = [structures.SiteHealth(
                    site_name = row['System Name'],
                    score = row['score'],
                    status = row['status'],
                    reasons = row['reason'].split(",") if row['reason'] else [],
                    metrics = structures.Metrics(
                        capacity_kw = row['Power (kW)'],
                        report_period_savings = row['Total Savings: Current Bill Period'],
                        operating_year_savings = row['Total Savings: Current Operating Year']))
                    for index, row in report.iterrows()]
    return site_health, report

def report_overview():
    report = read_report()
    overview = structures.OverAllMatrix(
        data_quality = data_quality_check(report),
        statistical_performance = statistical_analysis(report),
        site_wise_report = calculate_site_health(report))
    
    return overview.model_dump_json(indent = 2)

def rank_sites(report):
    savings_sorted = (report.sort_values(by='Total Savings: Current Bill Period', ascending=False).reset_index(drop=True))
    savings_sorted['rank'] = savings_sorted.index + 1
    return savings_sorted

def create_stat_matrix(report):
    return structures.PortfolioMetrics(
        total_sites = len(report),
        report_period_savings = report['Total Savings: Current Bill Period'].sum(),
        operating_year_savings = report['Total Savings: Current Operating Year'].sum(),
        negative_savings_site = len(report[report['Total Savings: Current Bill Period'] < 0]),
        sites_marked_healthy = len(report[report['status'] == 'Healthy']),
        sites_marked_average = len(report[report['status'] == 'Average']),
        sites_marked_needs_attention = len(report[report['status'] == 'Need Attention']),
        sites_marked_critical = len(report[report['status'] == 'Critical']),
        new_sites = len(report[report['status'] == 'New Site']))
     
def create_ai_ready_json():
    report = read_report()
    _, report = calculate_site_health(report)
    
    need_attention = report[report['status'] == 'Need Attention']
    critical = report[report['status'] == 'Critical']
    
    ai_json = structures.AIContent(
        report_period = "2026_06",
        portfolio = create_stat_matrix(report),
        data_quality= data_quality_check(report),
        top_performers= [structures.SiteMarker(site_name = row['System Name'],
                                                          savings = row['Total Savings: Current Bill Period'])
                                                          for index, row in (report[:5]).iterrows()], 
        sites_needing_attention= [structures.SiteMarker(site_name = row['System Name'],
                                                          reasons = row['reason'].split(",") if row['reason'] else [])
                                                          for index, row in need_attention.iterrows()],
        critical_sites= [structures.SiteMarker(site_name = row['System Name'],
                                                          reasons = row['reason'].split(",") if row['reason'] else [])
                                                          for index, row in critical.iterrows()])
    return ai_json.model_dump_json(indent= 2, exclude_none= True)