RPT_SUMMARY_PROMPT = """
                You are an expert business analyst.
                Summarize the following report.
                Report:\n{report}
                """

def savings_report_prompt(ai_context, facts_list):
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
            6. Use facts mentioned in {facts_list} for reasons or facts_type
            7. If there are no areas of concern, return an empty list.
            8. Return only the requested JSON structure.
            
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

def sementic_validatior(semantic_input):
    return f"""
            You are validating AI-generated site reasons against deterministic
            business reasons.
            
            For EACH site, compare its AI-generated reasons ONLY against the
            expected reasons for that SAME site.
            
            For EACH AI-generated reason:
            
            1. Find at most one expected reason with the same underlying
               business meaning.
            2. Set equivalent=true if the meanings are equivalent.
            3. Set equivalent=false if no expected reason has the same meaning.
            4. If equivalent=false, expected_reason must be null.
            5. Do not validate the entire list as a group.
            6. One matching reason must not cause another reason to be considered
               valid.
            7. Do not assume a reason is valid simply because it sounds similar.
            8. Ignore differences in capitalization, grammar and wording.
            9. Reasonable synonyms are allowed.
            10. Do not introduce business conditions that are not present in the
                expected reason.
            11. Return exactly one validation result for every AI-generated reason.
            12. Preserve the site_name exactly as provided.
            
            IMPORTANT:
            "Negative savings" and "low savings" are NOT automatically equivalent.
            "Zero savings" and "negative savings" are NOT equivalent.
            The underlying business condition must be the same.
            
            REASON DICTIONARY:
            {semantic_input}
            """