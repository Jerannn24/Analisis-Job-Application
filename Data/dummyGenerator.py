import os
import random
import pandas as pd
import numpy as np

# Seed
random.seed(42)
np.random.seed(42)

# Output folder
folder = "DummyData"
os.makedirs(folder, exist_ok=True)

# ========================
# 1. DEFINISI NAMA NYATA
# ========================
first_names = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eka', 'Fajar', 'Gita', 'Hadi', 'Indah', 'Joko',
               'Kiki', 'Lia', 'Mira', 'Nina', 'Oka', 'Putri', 'Qori', 'Rudi', 'Sari', 'Tono']
last_names = ['Santoso', 'Wibowo', 'Utami', 'Saputra', 'Wijaya', 'Halim', 'Ramadhan', 'Hernawan', 'Fauzi', 'Permata']

companies = ['Tokopedia', 'Bukalapak', 'Shopee', 'Gojek', 'Grab', 'Traveloka', 'Ruangguru', 'OVO', 'Zenius', 'Dana']
skills = ['Python', 'Java', 'SQL', 'C++', 'Go', 'HTML', 'CSS', 'JavaScript', 'PHP', 'R',
          'NodeJS', 'TypeScript', 'Kotlin', 'Swift', 'MongoDB', 'Firebase', 'Docker', 'Kubernetes', 'AWS', 'GCP']
languages = ['English', 'Indonesian', 'Japanese', 'Mandarin', 'Arabic']
schools = ['ITB', 'UI', 'UGM', 'Binus', 'Unpad', 'ITS', 'Telkom', 'IPB', 'Unair', 'UMN']
cities = ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Depok', 'Tangerang']
exp_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Manager', 'Director']
certifications = ['AWS Certified', 'Google Cloud Certified', 'Microsoft Certified', 'Cisco Certified', 'CompTIA Certified']
job_roles = ['Software Engineer', 'Data Scientist', 'Web Developer', 'Mobile Developer', 'DevOps Engineer',
              'UI/UX Designer', 'Product Manager', 'System Analyst', 'Network Engineer', 'Database Administrator']
GPA_levels = ['Cum Laude', 'Magna Cum Laude', 'Summa Cum Laude', 'With Honors', 'Regular']

# ========================
# 2. BUAT NODES
# ========================
applicants = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(50)]
jobs = [f"job_{i}" for i in range(20)]

nodes = []
nodes += [{'node': name, 'type': 'applicant'} for name in applicants]
nodes += [{'node': job, 'type': 'job'} for job in jobs]
nodes += [{'node': name, 'type': 'company'} for name in companies]
nodes += [{'node': skill, 'type': 'skill'} for skill in skills]
nodes += [{'node': lang, 'type': 'language'} for lang in languages]
nodes += [{'node': school, 'type': 'school'} for school in schools]
nodes += [{'node': city, 'type': 'city'} for city in cities]
nodes += [{'node': level, 'type': 'experience_level'} for level in exp_levels]
nodes += [{'node': cert, 'type': 'certification'} for cert in certifications]
nodes += [{'node': role, 'type': 'job_role'} for role in job_roles]
nodes += [{'node': gpa, 'type': 'GPA_level'} for gpa in GPA_levels]

nodes_df = pd.DataFrame(nodes)
nodes_df.to_csv(f"{folder}/nodes.csv", index=False)

# ========================
# 3. BUAT EDGES
# ========================
edges = []
for applicant in applicants:
    edges.append({'source': applicant, 'target': random.choice(schools), 'relation': 'attended'})
    edges.append({'source': applicant, 'target': random.choice(cities), 'relation': 'lives_in'})
    
    skill_count = random.randint(2, 4)
    selected_skills = random.sample(skills, skill_count)
    for skill in selected_skills:
        edges.append({'source': applicant, 'target': skill, 'relation': 'has_skill'})
        
    lang_count = random.randint(1, 2)
    selected_langs = random.sample(languages, lang_count)
    for lang in selected_langs:
        edges.append({'source': applicant, 'target': lang, 'relation': 'speaks'})
        
    applied_jobs = random.sample(jobs, random.randint(1, 3))
    for job in applied_jobs:
        edges.append({'source': applicant, 'target': job, 'relation': 'applied'})
        
    cert_count = random.randint(1, 2)
    selected_certs = random.sample(certifications, cert_count)
    for cert in selected_certs:
        edges.append({'source': applicant, 'target': cert, 'relation': 'has_certification'})

    edges.append({'source': applicant, 'target': random.choice(exp_levels), 'relation': 'has_experience_level'})
    edges.append({'source': applicant, 'target': random.choice(GPA_levels), 'relation': 'has_GPA_level'})
    

for job in jobs:
    edges.append({'source': job, 'target': random.choice(companies), 'relation': 'offered_by'})
    edges.append({'source': job, 'target': random.choice(cities), 'relation': 'located_in'})
    for _ in range(random.randint(2, 4)):
        edges.append({'source': job, 'target': random.choice(skills), 'relation': 'requires'})
    edges.append({'source': job, 'target': random.choice(exp_levels), 'relation': 'requires_experience_level'})
    edges.append({'source': job, 'target': random.choice(certifications), 'relation': 'requires_certification'})
    edges.append({'source': job, 'target': random.choice(job_roles), 'relation': 'is_job_role'})
    edges.append({'source': job, 'target': random.choice(GPA_levels), 'relation': 'requires_GPA_level'})
    
edges_df = pd.DataFrame(edges)
edges_df.to_csv(f"{folder}/edges.csv", index=False)

# ========================
# 4. BUAT LABELS
# ========================
labels = []
applied_edges = edges_df[edges_df['relation'] == 'applied'].sample(frac=0.6, random_state=42)
for edge in applied_edges.itertuples():
    labels.append({
        'applicant': edge.source,
        'job': edge.target,
        'accepted': random.choice([0, 1])
    })

labels_df = pd.DataFrame(labels)
labels_df.to_csv(f"{folder}/labels.csv", index=False)

folder, len(nodes_df), len(edges_df), len(labels_df)
