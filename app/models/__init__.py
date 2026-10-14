# Import all models so Alembic can discover them. Preserve any existing imports.
from app.models.core import User, Resume, ProcessingJob
from app.models.career import CareerProfile, Experience, Education, Certification, Project, Skill, UserSkill, ResumeExtraction
