#!/usr/bin/env python3
"""
Script to generate separate HTML pages for each section.
Each page will have the full styling but only show that section's content.
"""

import re
import os

# Read the main index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract sections
sections = {
    'writing': {
        'id': 'writing',
        'title': 'Writing',
        'start': content.find('<section class="content-section" id="writing">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="writing">')) + 10
    },
    'research': {
        'id': 'research',
        'title': 'Research',
        'start': content.find('<section class="content-section" id="research">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="research">')) + 10
    },
    'robotics': {
        'id': 'robotics',
        'title': 'Engineering and Robotics',
        'start': content.find('<section class="content-section" id="robotics">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="robotics">')) + 10
    },
    'music': {
        'id': 'music',
        'title': 'Music',
        'start': content.find('<section class="content-section" id="music">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="music">')) + 10
    },
    'cheerleading': {
        'id': 'cheerleading',
        'title': 'Cheerleading',
        'start': content.find('<section class="content-section" id="cheerleading">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="cheerleading">')) + 10
    },
    'art-podcast': {
        'id': 'art-podcast',
        'title': 'Art & Podcast',
        'start': content.find('<section class="content-section" id="art-podcast">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="art-podcast">')) + 10
    },
    'education': {
        'id': 'education',
        'title': 'Education & Academics',
        'start': content.find('<section class="content-section" id="education">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="education">')) + 10
    },
    'skills': {
        'id': 'skills',
        'title': 'Skills, Languages, and Interests',
        'start': content.find('<section class="content-section" id="skills">'),
        'end': content.find('</section>', content.find('<section class="content-section" id="skills">')) + 10
    }
}

# Extract parts of the HTML
head_end = content.find('</head>')
body_start = content.find('<body>')
body_end = content.find('</body>')
scripts = content[body_end:content.find('</html>')]

# Get styles (everything in <style> tag)
style_start = content.find('<style>')
style_end = content.find('</style>') + 8
styles = content[style_start:style_end]

# Get navbar HTML
navbar_start = content.find('<!-- Navbar -->')
navbar_end = content.find('</nav>', navbar_start) + 6
navbar_html = content[navbar_start:navbar_end]

# Get footer HTML
footer_start = content.find('<!-- Footer -->')
footer_end = content.find('</footer>', footer_start) + 8
footer_html = content[footer_start:footer_end]

# Get lightbox HTML
lightbox_start = content.find('<!-- Lightbox Modal -->')
lightbox_end = content.find('</div>', content.find('<div id="lightbox"')) + 6
lightbox_html = content[lightbox_start:lightbox_end]

# Get stage and rail HTML (for boot animation)
stage_start = content.find('<div class="stage">')
stage_before_site = content.find('<main id="site"', stage_start)
stage_html = content[stage_start:stage_before_site]

# Get hero section
hero_start = content.find('<section class="hero-section"')
hero_end = content.find('</section>', hero_start) + 10
hero_html = content[hero_start:hero_end]

# Generate pages for each section
for section_key, section_info in sections.items():
    if section_info['start'] == -1:
        print(f"Warning: Section {section_key} not found, skipping...")
        continue
    
    section_content = content[section_info['start']:section_info['end']]
    
    # Update media paths
    section_content = section_content.replace('src="media/', 'src="../media/')
    section_content = section_content.replace("url('media/", "url('../media/")
    section_content = section_content.replace('style="background-image:url(\'media/', 'style="background-image:url(\'../media/')
    
    # Create navbar with navigation links for section pages
    navbar_with_links = navbar_html.replace('href="#about"', 'href="../index.html"').replace('src="media/', 'src="../media/')
    
    # Update navigation link paths to use relative paths
    navbar_with_links = navbar_with_links.replace('href="/music"', 'href="../music"')
    navbar_with_links = navbar_with_links.replace('href="/research"', 'href="../research"')
    navbar_with_links = navbar_with_links.replace('href="/education"', 'href="../education"')
    navbar_with_links = navbar_with_links.replace('href="/cheerleading"', 'href="../cheerleading"')
    navbar_with_links = navbar_with_links.replace('href="/art-podcast"', 'href="../art-podcast"')
    
    # Remove duplicate comment from navbar if present
    if navbar_with_links.startswith('<!-- Navbar -->'):
        navbar_with_links = navbar_with_links.replace('<!-- Navbar -->', '', 1)
    
    # Create the page HTML
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Stella Xulin — {section_info['title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&display=swap" rel="stylesheet">
{styles}
</head>
<body>
  <!-- Navbar -->
{navbar_with_links}

  <div class="stage">
{stage_html}
    <main id="site" class="site" aria-hidden="true">
      <div class="content">
{section_content}
      </div>

      <!-- Footer -->
{footer_html.replace('src="media/', 'src="../media/')}
    </main>
  </div>

  <!-- Lightbox Modal -->
{lightbox_html}

{scripts.replace('src="media/', 'src="../media/')}
  <script>
    // Skip boot animation for section pages - show content immediately
    (function () {{
      const site = document.getElementById('site');
      const navbar = document.getElementById('navbar');
      const stage = document.querySelector('.stage');
      const railWrap = document.querySelector('.rail-wrap');
      
      // Hide boot animation immediately
      if (railWrap) {{
        railWrap.style.display = 'none';
      }}
      
      // Show content immediately
      stage.classList.add('site-mode');
      site.classList.add('show');
      site.removeAttribute('aria-hidden');
      
      if (navbar) {{
        navbar.classList.add('show');
      }}
    }})();
  </script>
</body>
</html>"""
    
    # Write to file
    folder_path = section_key
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'index.html')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    
    print(f"Created {file_path}")

print("All section pages created successfully!")

