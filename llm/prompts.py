RPT_SUMMARY_PROMPT = """
                You are an expert business analyst.
                Summarize the following report.
                Report:\n{report}
                """

def savings_report_prompt(ai_context):
    return f"""
            You are an expert business analyst reviewing a monthly savings report.
            
            Analyze the provided report context and generate a concise, 
            stakeholder-friendly summary of the portfolio's performance.
            
            STRICT RULES:
            1. Use only the information provided in the Report Context.
            2. Do not invent, assume, or infer facts that are not explicitly provided.
            3. Do not introduce external knowledge or information.
            4. Recommendations must be directly supported by the provided data.
            5. Prioritize the most important findings rather than repeating all metrics.
            6. If there are no areas of concern, return an empty list.
            7. Return only the requested JSON structure.
            
            OUTPUT FORMAT:
            {{
                "overall_assessment": "string, maximum 200 words",
                "key_findings": ["string", "..."],
                "areas_of_concern": [
                    {{
                        "site_name": "string",
                        "reasons": ["string", "..."]
                    }}
                ],
                "positive_highlights": ["string", "..."],
                "recommendations": ["string", "..."]
            }}
            
            LIMITS:
            - key_findings: maximum 5 items
            - positive_highlights: maximum 5 items
            - recommendations: maximum 5 items
            
            REPORT CONTEXT:
            {ai_context}
            """