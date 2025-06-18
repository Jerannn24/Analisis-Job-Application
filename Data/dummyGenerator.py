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
               'Kiki', 'Lia', 'Mira', 'Nina', 'Oka', 'Putri', 'Qori', 'Rudi', 'Sari', 'Tono', 'Umi',
               'Vina', 'Wawan', 'Xena', 'Yani', 'Zaki', 'Ayu', 'Bima', 'Cahya', 'Dimas', 'Eko', 'Fika',
               'Gilang', 'Hana', 'Ika', 'Jaya', 'Kirana', 'Lutfi', 'Maya', 'Nanda', 'Omar', 'Puti']
last_names = ['Santoso', 'Wibowo', 'Utami', 'Saputra', 'Wijaya', 'Halim', 'Ramadhan', 'Hernawan', 'Fauzi', 'Permata', 'Suryanto',
               'Prabowo', 'Sihombing', 'Gunawan', 'Lestari', 'Nugroho', 'Siregar', 'Yulianto', 'Kusuma', 'Hidayat', 'Purnama','aditya',
               'Prasetyo', 'Sutrisno', 'Wulandari', 'Siregar', 'Haryanto', 'Larasati', 'Prabuwono', 'Kurniawan', 'Sukmawati', 'Wicaksono',
               'Sutanto', 'Wicaksono', 'Prabowo', 'Haryanto', 'Lestari', 'Nugroho', 'Siregar', 'Yulianto', 'Kusuma', 'Hidayat', 'Purnama']

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
# NODE GENERATION
# ========================
applicants = [f"{fn} {ln}" for fn in first_names for ln in last_names]
jobs = [f"job_{i}" for i in range(10)]

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
# EDGE GENERATION
# ========================
edges = []
for applicant in applicants:
    edges.append({'source': applicant, 'target': random.choice(schools), 'relation': 'attended'})
    edges.append({'source': applicant, 'target': random.choice(cities), 'relation': 'lives_in'})
    edges.append({'source': applicant, 'target': random.choice(exp_levels), 'relation': 'has_experience_level'})
    edges.append({'source': applicant, 'target': random.choice(GPA_levels), 'relation': 'has_GPA_level'})

    for skill in random.sample(skills, 3):
        edges.append({'source': applicant, 'target': skill, 'relation': 'has_skill'})

    for lang in random.sample(languages, 1):
        edges.append({'source': applicant, 'target': lang, 'relation': 'speaks'})

    for cert in random.sample(certifications, 1):
        edges.append({'source': applicant, 'target': cert, 'relation': 'has_certification'})

# Hubungan job
for job in jobs:
    edges.append({'source': job, 'target': random.choice(companies), 'relation': 'offered_by'})
    edges.append({'source': job, 'target': random.choice(cities), 'relation': 'located_in'})
    edges.append({'source': job, 'target': random.choice(exp_levels), 'relation': 'requires_experience_level'})
    edges.append({'source': job, 'target': random.choice(certifications), 'relation': 'requires_certification'})
    edges.append({'source': job, 'target': random.choice(job_roles), 'relation': 'is_job_role'})
    edges.append({'source': job, 'target': random.choice(GPA_levels), 'relation': 'requires_GPA_level'})

    for skill in random.sample(skills, 3):
        edges.append({'source': job, 'target': skill, 'relation': 'requires'})

edges_df = pd.DataFrame(edges)

# ========================
# LAMARAN & LABELS (REALISTIK)
# ========================
labels = []

for applicant in applicants:
    applied_jobs = random.sample(jobs, 2)
    for job in applied_jobs:
        edges.append({'source': applicant, 'target': job, 'relation': 'applied'})

        # Ambil skill applicant
        applicant_skills = set(
            edge['target'] for edge in edges
            if edge['source'] == applicant and edge['relation'] == 'has_skill'
        )

        # Ambil skill yang dibutuhkan oleh job
        job_skills = set(
            edge['target'] for edge in edges
            if edge['source'] == job and edge['relation'] == 'requires'
        )

        # Hitung overlap skill
        skill_overlap = len(applicant_skills & job_skills)

        # Simulasikan diterima atau tidak berdasarkan overlap skill
        acceptance_prob = 0.4 + 0.2 * skill_overlap  # 0.2 baseline + 0.2 per skill match
        accepted = 1 if random.random() < acceptance_prob else 0

        labels.append({'applicant': applicant, 'job': job, 'accepted': accepted})

# Simpan CSV
edges_df = pd.DataFrame(edges)
edges_df.to_csv(f"{folder}/edges.csv", index=False)

labels_df = pd.DataFrame(labels)
labels_df.to_csv(f"{folder}/labels.csv", index=False)

folder, len(nodes_df), len(edges_df), len(labels_df)
