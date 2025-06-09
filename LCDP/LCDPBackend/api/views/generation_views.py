import os
import json
import zipfile
import tempfile
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Project, Page


def generate_react_component(component):
    """
    Generate React component code based on component data
    """
    component_type = component.get('type', 'div')
    props = component.get('props', {})
    
    # Helper function to safely convert to int
    def safe_int(value, default=0):
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    # Helper function to safely convert to string
    def safe_str(value, default=''):
        try:
            return str(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    # Basic component mapping
    component_map = {
        'Button': f"<button style={{{{color: '{safe_str(props.get('color', '#4F46E5'))}'}}}}>{safe_str(props.get('label', 'Button'))}</button>",
        'Input': f"<input type=\"{safe_str(props.get('type', 'text'))}\" placeholder=\"{safe_str(props.get('placeholder', ''))}\" defaultValue=\"{safe_str(props.get('value', ''))}\" />",
        'Text': f"<p style={{{{color: '{safe_str(props.get('color', '#374151'))}', fontSize: '{safe_str(props.get('fontSize', 'medium'))}'}}}}>{safe_str(props.get('value', 'Text'))}</p>",
        'Image': f"<img src=\"{safe_str(props.get('src', ''))}\" alt=\"{safe_str(props.get('alt', ''))}\" style={{{{borderRadius: '{safe_int(props.get('borderRadius', 0))}px'}}}} />",
        'Container': f"<div style={{{{backgroundColor: '{safe_str(props.get('backgroundColor', '#ffffff'))}', padding: '{safe_int(props.get('padding', 16))}px', borderRadius: '{safe_int(props.get('borderRadius', 8))}px'}}}}></div>",
        'Progress': f"<div style={{{{width: '100%', backgroundColor: '#e5e7eb', borderRadius: '4px'}}}}><div style={{{{width: '{safe_int(props.get('value', 0))}%', backgroundColor: '{safe_str(props.get('color', '#4F46E5'))}', height: '8px', borderRadius: '4px'}}}}></div></div>",
        'Rating': f"<div>{'⭐' * safe_int(props.get('value', 0))}</div>",
    }
    
    return component_map.get(component_type, f"<div>Unsupported component: {component_type}</div>")


def generate_react_page(page_data, page_name):
    """
    Generate a React page component from page data
    """
    components = page_data.get('layout_config', {}).get('components', [])
    
    component_jsx_parts = []
    for i, comp in enumerate(components):
        component_jsx_parts.append(
            f'<div key="{comp.get("id", i)}" style={{{{ position: "absolute", left: "{comp.get("x", 0) * 100}px", top: "{comp.get("y", 0) * 60}px", width: "{comp.get("w", 2) * 100}px", height: "{comp.get("h", 1) * 60}px" }}}}>'
        )
        component_jsx_parts.append(f'        {generate_react_component(comp)}')
        component_jsx_parts.append('      </div>')
    
    component_jsx = '\n      '.join(component_jsx_parts)
    
    return f'''import React from 'react';

function {page_name.replace(' ', '')}Page() {{
  return (
    <div style={{{{ position: 'relative', width: '100%', minHeight: '100vh', backgroundColor: '#f9fafb' }}}}>
      {component_jsx}
    </div>
  );
}}

export default {page_name.replace(' ', '')}Page;
'''


def generate_react_app(project, pages):
    """
    Generate a complete React application
    """
    
    # Generate App.js
    page_imports = '\n'.join([f"import {page.name.replace(' ', '')}Page from './pages/{page.name.replace(' ', '')}Page';" for page in pages])
    page_routes = '\n        '.join([f'<Route path="/{page.name.lower().replace(" ", "-")}" element={{<{page.name.replace(" ", "")}Page />}} />' for page in pages])
    
    page_links = []
    for page in pages:
        page_links.append(f'<Link to="/{page.name.lower().replace(" ", "-")}" style={{{{ marginRight: "10px", color: "#3b82f6" }}}}>{page.name}</Link>')
    page_links_str = ' | '.join(page_links)
    
    app_js = f'''import React from 'react';
import {{ BrowserRouter as Router, Routes, Route, Link }} from 'react-router-dom';
{page_imports}

function App() {{
  return (
    <Router>
      <div className="App">
        <nav style={{{{ padding: '20px', backgroundColor: '#f3f4f6', borderBottom: '1px solid #e5e7eb' }}}}>
          <h1 style={{{{ margin: 0, color: '#1f2937' }}}}>{project.name}</h1>
          <div style={{{{ marginTop: '10px' }}}}>
            {page_links_str}
          </div>
        </nav>
        <main style={{{{ padding: '20px' }}}}>
          <Routes>
            <Route path="/" element={{<{pages[0].name.replace(' ', '')}Page />}} />
            {page_routes}
          </Routes>
        </main>
      </div>
    </Router>
  );
}}

export default App;
'''

    # Generate package.json
    package_json = {
        "name": project.name.lower().replace(' ', '-'),
        "version": "1.0.0",
        "description": f"Generated app for {project.name}",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.1",
            "react-scripts": "5.0.1"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }

    # Generate index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''

    # Generate index.html
    index_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Generated app for {project.name}" />
    <title>{project.name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''

    # Generate README.md
    readme_md = f'''# {project.name}

This is a React application generated from your LCDP project.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### `npm run build`

Builds the app for production to the `build` folder.

### `npm test`

Launches the test runner in interactive watch mode.

## Deployment

This project was generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} from LCDP.

You can deploy this app to any static hosting service like Vercel, Netlify, or GitHub Pages.
'''

    return {
        'App.js': app_js,
        'package.json': json.dumps(package_json, indent=2),
        'src/index.js': index_js,
        'public/index.html': index_html,
        'README.md': readme_md
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_project(request, project_id):
    """
    Generate downloadable application from project
    """
    try:
        # Get project and verify ownership
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        
        # Get all pages for this project
        pages = Page.objects.filter(project=project)
        
        if not pages.exists():
            return Response({
                'error': 'No pages found in this project. Please create some pages first.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate application files
        app_files = generate_react_app(project, pages)
        
        # Generate page files
        page_files = {}
        for page in pages:
            # Create page data dictionary with proper layout_config access
            page_data = {
                'layout_config': page.layout_config if page.layout_config else {'components': []}
            }
            page_content = generate_react_page(page_data, page.name)
            page_files[f'src/pages/{page.name.replace(" ", "")}Page.js'] = page_content
        
        # Create a temporary zip file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add app files
                for file_path, content in app_files.items():
                    zipf.writestr(file_path, content)
                
                # Add page files
                for file_path, content in page_files.items():
                    zipf.writestr(file_path, content)
                
                # Create pages directory structure
                zipf.writestr('src/pages/', '')
            
            # Read the zip file content
            tmp_file.seek(0)
            with open(tmp_file.name, 'rb') as f:
                zip_content = f.read()
        
        # Clean up temp file
        os.unlink(tmp_file.name)
        
        # Return the zip file as download
        response = HttpResponse(zip_content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{project.name.replace(" ", "_")}_app.zip"'
        response['Content-Length'] = len(zip_content)
        
        return response
        
    except Exception as e:
        return Response({
            'error': f'Generation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generation_status(request, project_id):
    """
    Get generation status (for future async generation)
    """
    try:
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        pages_count = Page.objects.filter(project=project).count()
        
        return Response({
            'project_id': project_id,
            'project_name': project.name,
            'pages_count': pages_count,
            'can_generate': pages_count > 0,
            'status': 'ready'
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 