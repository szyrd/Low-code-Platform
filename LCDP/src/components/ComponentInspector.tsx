import React from 'react';
import { ComponentData } from '../types/types';

interface ComponentInspectorProps {
  selectedComponent: ComponentData | null;
  onPropertyChange: (id: string, propName: string, value: any) => void;
}

const ComponentInspector: React.FC<ComponentInspectorProps> = ({ 
  selectedComponent, 
  onPropertyChange 
}) => {
  if (!selectedComponent) {
    return <div className="inspector-panel">Select a component to edit its properties</div>;
  }

  const handlePropertyChange = (propName: string) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    onPropertyChange(selectedComponent.id, propName, e.target.value);
  };

  // Common properties for all components
  const renderCommonProperties = () => (
    <>
      <div className="property-group">
        <h4>Position & Size</h4>
        <div className="property-field">
          <label>X Position:</label>
          <input 
            type="number" 
            value={selectedComponent.x} 
            onChange={handlePropertyChange('x')} 
            disabled 
          />
        </div>
        <div className="property-field">
          <label>Y Position:</label>
          <input 
            type="number" 
            value={selectedComponent.y} 
            onChange={handlePropertyChange('y')} 
            disabled 
          />
        </div>
        <div className="property-field">
          <label>Width:</label>
          <input 
            type="number" 
            value={selectedComponent.w} 
            onChange={handlePropertyChange('w')} 
            disabled 
          />
        </div>
        <div className="property-field">
          <label>Height:</label>
          <input 
            type="number" 
            value={selectedComponent.h} 
            onChange={handlePropertyChange('h')} 
            disabled 
          />
        </div>
      </div>
    </>
  );

  // Render component-specific properties based on type
  const renderComponentProperties = () => {
    switch (selectedComponent.type) {
      case 'Button':
        return (
          <div className="property-group">
            <h4>Button Properties</h4>
            <div className="property-field">
              <label>Label:</label>
              <input 
                type="text" 
                value={selectedComponent.props.label || ''} 
                onChange={handlePropertyChange('props.label')} 
              />
            </div>
            <div className="property-field">
              <label>Color:</label>
              <input 
                type="text" 
                value={selectedComponent.props.color || ''} 
                onChange={handlePropertyChange('props.color')} 
              />
            </div>
          </div>
        );
      case 'Input':
        return (
          <div className="property-group">
            <h4>Input Properties</h4>
            <div className="property-field">
              <label>Placeholder:</label>
              <input 
                type="text" 
                value={selectedComponent.props.placeholder || ''} 
                onChange={handlePropertyChange('props.placeholder')} 
              />
            </div>
            <div className="property-field">
              <label>Default Value:</label>
              <input 
                type="text" 
                value={selectedComponent.props.value || ''} 
                onChange={handlePropertyChange('props.value')} 
              />
            </div>
          </div>
        );
      case 'Text':
        return (
          <div className="property-group">
            <h4>Text Properties</h4>
            <div className="property-field">
              <label>Text:</label>
              <input 
                type="text" 
                value={selectedComponent.props.value || ''} 
                onChange={handlePropertyChange('props.value')} 
              />
            </div>
            <div className="property-field">
              <label>Color:</label>
              <input 
                type="text" 
                value={selectedComponent.props.color || ''} 
                onChange={handlePropertyChange('props.color')} 
              />
            </div>
          </div>
        );
      case 'Table':
        return (
          <div className="property-group">
            <h4>Table Properties</h4>
            <div className="property-field">
              <label>Column Headers (JSON):</label>
              <textarea 
                value={JSON.stringify(selectedComponent.props.columns || [])} 
                onChange={(e) => {
                  try {
                    const value = JSON.parse(e.target.value);
                    onPropertyChange(selectedComponent.id, 'props.columns', value);
                  } catch (error) {
                    // Invalid JSON, don't update
                  }
                }}
              />
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="inspector-panel">
      <h3>Component Inspector</h3>
      <div className="property-field">
        <label>Component Type:</label>
        <input type="text" value={selectedComponent.type} disabled />
      </div>
      <div className="property-field">
        <label>Component ID:</label>
        <input type="text" value={selectedComponent.id} disabled />
      </div>
      
      {renderCommonProperties()}
      {renderComponentProperties()}
    </div>
  );
};

export default ComponentInspector; 