import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ReactGridLayout, { WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import ComponentRenderer from './ComponentRenderer';
import ComponentInspector from './ComponentInspector';
import { ComponentData, LayoutData } from '../types/types';
import { savePage } from '../services/api';
import './UIBuilder.css';

// Enable responsive features
const GridLayout = WidthProvider(ReactGridLayout);

// Available component types
const componentTypes = ['Button', 'Input', 'Text', 'Table'];

// Default properties for new components
const getDefaultProps = (type: string) => {
  switch (type) {
    case 'Button':
      return { label: 'Button', color: 'blue' };
    case 'Input':
      return { placeholder: 'Enter text...', value: '' };
    case 'Text':
      return { value: 'Text', color: 'black' };
    case 'Table':
      return { 
        columns: [
          { key: 'id', header: 'ID' },
          { key: 'name', header: 'Name' }
        ],
        data: [
          { id: 1, name: 'Item 1' },
          { id: 2, name: 'Item 2' }
        ]
      };
    default:
      return {};
  }
};

// Component initial size
const getDefaultSize = (type: string) => {
  switch (type) {
    case 'Button':
      return { w: 2, h: 1 };
    case 'Input':
      return { w: 3, h: 1 };
    case 'Text':
      return { w: 3, h: 1 };
    case 'Table':
      return { w: 6, h: 4 };
    default:
      return { w: 2, h: 1 };
  }
};

const UIBuilder: React.FC = () => {
  const [components, setComponents] = useState<ComponentData[]>([]);
  const [selectedComponent, setSelectedComponent] = useState<ComponentData | null>(null);
  const [pageName, setPageName] = useState<string>('New Page');
  const [isSaving, setIsSaving] = useState<boolean>(false);

  // Handle dropping a new component onto the canvas
  const handleDrop = (type: string) => {
    const id = uuidv4();
    const defaultSize = getDefaultSize(type);
    
    const newComponent: ComponentData = {
      id,
      type: type as ComponentData['type'],
      x: 0, // Default x position
      y: 0, // Will be adjusted by the grid
      w: defaultSize.w,
      h: defaultSize.h,
      props: getDefaultProps(type)
    };

    setComponents([...components, newComponent]);
    setSelectedComponent(newComponent);
  };

  // Handle component selection
  const handleSelectComponent = (id: string) => {
    const component = components.find(c => c.id === id);
    setSelectedComponent(component || null);
  };

  // Handle layout changes from react-grid-layout
  const handleLayoutChange = (layout: ReactGridLayout.Layout[]) => {
    const updatedComponents = components.map(component => {
      const layoutItem = layout.find(item => item.i === component.id);
      if (layoutItem) {
        return {
          ...component,
          x: layoutItem.x,
          y: layoutItem.y,
          w: layoutItem.w,
          h: layoutItem.h
        };
      }
      return component;
    });

    setComponents(updatedComponents);
    
    // Update selected component if needed
    if (selectedComponent) {
      const updatedSelectedComponent = updatedComponents.find(c => c.id === selectedComponent.id);
      setSelectedComponent(updatedSelectedComponent || null);
    }
  };

  // Handle property changes in the inspector
  const handlePropertyChange = (id: string, propPath: string, value: any) => {
    const updatedComponents = components.map(component => {
      if (component.id === id) {
        // Handle nested props with dot notation (e.g. 'props.label')
        if (propPath.startsWith('props.')) {
          const propName = propPath.replace('props.', '');
          return {
            ...component,
            props: {
              ...component.props,
              [propName]: value
            }
          };
        } else {
          // Handle direct component properties (x, y, w, h)
          return {
            ...component,
            [propPath]: value
          };
        }
      }
      return component;
    });

    setComponents(updatedComponents);
    
    // Update selected component
    if (selectedComponent && selectedComponent.id === id) {
      const updatedSelectedComponent = updatedComponents.find(c => c.id === id);
      setSelectedComponent(updatedSelectedComponent || null);
    }
  };

  // Delete the selected component
  const handleDeleteComponent = () => {
    if (selectedComponent) {
      const updatedComponents = components.filter(c => c.id !== selectedComponent.id);
      setComponents(updatedComponents);
      setSelectedComponent(null);
    }
  };

  // Save the page layout to the backend
  const handleSavePage = async () => {
    if (components.length === 0) {
      alert('Cannot save an empty page. Add some components first.');
      return;
    }

    const pageData: LayoutData = {
      name: pageName,
      components: components
    };

    setIsSaving(true);
    try {
      await savePage(pageData);
      alert('Page saved successfully!');
    } catch (error) {
      alert('Failed to save page. Please try again.');
      console.error('Error saving page:', error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="ui-builder">
      <div className="header">
        <input 
          type="text"
          className="page-name-input"
          value={pageName}
          onChange={(e) => setPageName(e.target.value)}
          placeholder="Enter page name"
        />
        <button 
          className="save-button"
          onClick={handleSavePage}
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save Page'}
        </button>
      </div>

      <div className="main-content">
        <div className="component-sidebar">
          <h3>Components</h3>
          <div className="component-list">
            {componentTypes.map(type => (
              <div 
                key={type}
                className="component-item"
                draggable
                onDragEnd={() => handleDrop(type)}
              >
                {type}
              </div>
            ))}
          </div>
        </div>

        <div className="canvas">
          <GridLayout
            className="layout"
            cols={12}
            rowHeight={50}
            onLayoutChange={handleLayoutChange}
            draggableHandle=".component-handle"
          >
            {components.map(component => (
              <div 
                key={component.id} 
                data-grid={{ 
                  x: component.x, 
                  y: component.y, 
                  w: component.w, 
                  h: component.h,
                  i: component.id
                }}
                className={`component-wrapper ${selectedComponent?.id === component.id ? 'selected' : ''}`}
                onClick={() => handleSelectComponent(component.id)}
              >
                <div className="component-handle">
                  {component.type}
                </div>
                <ComponentRenderer component={component} />
              </div>
            ))}
          </GridLayout>
          {components.length === 0 && (
            <div className="empty-canvas-message">
              Drag and drop components from the sidebar to get started
            </div>
          )}
        </div>

        <div className="inspector">
          <ComponentInspector 
            selectedComponent={selectedComponent}
            onPropertyChange={handlePropertyChange}
          />
          {selectedComponent && (
            <button 
              className="delete-button"
              onClick={handleDeleteComponent}
            >
              Delete Component
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default UIBuilder; 