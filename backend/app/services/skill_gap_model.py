class SkillGapModel:

    def __init__(self):
        pass

    def compute_gap(self, candidate_skills: list, job_skills: list):
        """
        Receives:
        - candidate_skills: array of strings
        - job_skills: array of strings (directly from FAISS job object)

        Returns:
        matched_skills, missing_skills, match_percent
        """
        cand = set([s.lower() for s in candidate_skills])
        req = set([s.lower() for s in job_skills])

        matched = sorted(list(cand.intersection(req)))
        missing = sorted(list(req - cand))

        match_percent = 0
        if len(req) > 0:
            match_percent = round(len(matched) / len(req) * 100, 2)

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_percent": match_percent
        }

    def analyze_single(self, candidate, job):
        """
        INPUT:
          candidate = { "candidate_skills": [...] }
          job       = { "job_title": "...", "skills_required": [...], "similarity_score": 0.82 }

        OUTPUT:
          Unified result object
        """
        candidate_skills = candidate["candidate_skills"]
        job_skills = job["skills_required"]

        gap = self.compute_gap(candidate_skills, job_skills)

        return {
            "job_id": job.get("job_id"),
            "job_title": job.get("job_title"),
            "similarity_score": job.get("similarity_score"),

            "skills_required": job_skills,
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "match_percent": gap["match_percent"]
        }

    def analyze_multiple(self, candidate, jobs: list):
        """
        INPUT:
          candidate = { "candidate_skills": [...] }
          jobs = [ job_obj1, job_obj2, job_obj3, ... ]

        OUTPUT:
          List of computed skill gaps
        """
        results = []
        for job in jobs:
            results.append(self.analyze_single(candidate, job))
        return results
