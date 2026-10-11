import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data and define mapping
df = pd.read_csv('projects.csv')

mapping = {
    'Software Development': 'Software & AI Development', 'Software Dev': 'Software & AI Development',
    'Development': 'Software & AI Development', 'AI Development': 'Software & AI Development',
    'Web Development': 'Software & AI Development', 'Game Development': 'Software & AI Development',
    'AI Integration': 'Software & AI Development', 'Tool Integration': 'Software & AI Development',
    'AI Framework Support': 'Software & AI Development', 'AI Framework': 'Software & AI Development',
    'AI / QA': 'Software & AI Development', 'Database Management': 'Software & AI Development',
    'Database Interaction': 'Software & AI Development', 'Cybersecurity': 'Software & AI Development',
    
    'Productivity': 'Productivity & Automation', 'Workflow Automation': 'Productivity & Automation',
    'Planning & Dev': 'Productivity & Automation', 'Collaboration': 'Productivity & Automation',
    'Problem Solving': 'Productivity & Automation', 'Information Retrieval': 'Productivity & Automation',
    'Documentation': 'Productivity & Automation', 'Knowledge Management': 'Productivity & Automation',
    'Workflow Orchestration': 'Productivity & Automation', 'Intelligent Agents': 'Productivity & Automation',
    'Performance Evaluation': 'Productivity & Automation', 'Monitoring & Analytics': 'Productivity & Automation',
    'Data Extraction': 'Productivity & Automation', 'Data Analysis': 'Productivity & Automation',
    'Communication': 'Productivity & Automation',
    
    'Entertainment': 'Media & Entertainment', 'Gaming': 'Media & Entertainment',
    'Creative Writing': 'Media & Entertainment', 'Media & Content': 'Media & Entertainment',
    'Media & Journalism': 'Media & Entertainment', 'Media & News': 'Media & Entertainment',
    'Publishing & Media': 'Media & Entertainment', 'Multimedia AI': 'Media & Entertainment',
    'Image Processing': 'Media & Entertainment', 'Audio Processing': 'Media & Entertainment',
    
    'Human Resources': 'Business & Legal Services', 'Recruitment': 'Business & Legal Services',
    'Legal': 'Business & Legal Services', 'Legal Tech': 'Business & Legal Services',
    'Privacy/Compliance': 'Business & Legal Services', 'Real Estate': 'Business & Legal Services',
    
    'Education': 'Education & Research', 'Education / Research': 'Education & Research',
    'Research': 'Education & Research', 'Cognitive Sciences': 'Education & Research',
    
    'Retail': 'Retail & Supply Chain', 'E-commerce': 'Retail & Supply Chain', 'Supply Chain': 'Retail & Supply Chain',
    'Manufacturing': 'Industrial & Other', 'Agriculture': 'Industrial & Other',
    'Energy': 'Industrial & Other', 'Transportation': 'Industrial & Other',
    
    'Sales': 'Sales & Marketing', 'Marketing': 'Sales & Marketing', 'Social Media': 'Sales & Marketing',
    
    'Hospitality': 'Travel & Hospitality', 'Travel': 'Travel & Hospitality', 'Food & Culinary': 'Travel & Hospitality',
    
    'Customer Service': 'Customer Support', 'Customer Support': 'Customer Support',
    'Healthcare': 'Healthcare', 'Health Insurance': 'Healthcare',
    'Finance': 'Finance'
}

df['clean_category'] = df['industry'].map(mapping)

# --- CHART 1: Category Counts ---
counts = df['clean_category'].value_counts().sort_values(ascending=True)

plt.figure(figsize=(10, 6.5))
bars = plt.barh(counts.index, counts.values, color='#2c3e50')

for bar in bars:
    plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
             f'{int(bar.get_width())}', va='center', ha='left', fontsize=10)

plt.title("In the README's 112 listed projects, about half\nare productivity or software engineering tools.", 
          fontsize=14, pad=20, loc='left', fontweight='bold')
plt.xlabel('Number of Projects', fontsize=11)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.subplots_adjust(left=0.25, right=0.95, top=0.85, bottom=0.15) 
plt.figtext(0.05, 0.02, 'Source: README tables of ashishpatel26/500-AI-Agents-Projects (112 listed entries; repo title says 500+), Oct 2026.', 
            ha='left', fontsize=9, color='gray')
plt.show()

# --- CHART 2: Stacked by Framework ---
pivot_df = df.groupby(['clean_category', 'framework']).size().unstack(fill_value=0)
pivot_df['Total'] = pivot_df.sum(axis=1)
pivot_df = pivot_df.sort_values('Total', ascending=True).drop('Total', axis=1)

ax = pivot_df.plot(kind='barh', stacked=True, figsize=(12, 7.5), colormap='viridis', width=0.8)
plt.title("Which AI agent categories each framework's examples cover.", 
          fontsize=14, pad=20, loc='left', fontweight='bold')
plt.xlabel('Number of Projects', fontsize=11)
plt.ylabel('')
plt.legend(title='Framework', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.subplots_adjust(left=0.2, right=0.85, top=0.85, bottom=0.15)
plt.figtext(0.05, 0.02, 'Source: README tables of ashishpatel26/500-AI-Agents-Projects (112 listed entries; repo title says 500+), Oct 2026.', 
            ha='left', fontsize=9, color='gray')
plt.show()