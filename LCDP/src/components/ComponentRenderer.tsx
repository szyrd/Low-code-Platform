import React from 'react';
import { ComponentData } from '../types/types';
import { Button, Input, Text, Table } from './DraggableComponents';

interface ComponentRendererProps {
  component: ComponentData;
}

const ComponentRenderer: React.FC<ComponentRendererProps> = ({ component }) => {
  const { type, props } = component;

  // Render the appropriate component based on type
  switch (type) {
    case 'Button':
      return <Button {...props} />;
    case 'Input':
      return <Input {...props} />;
    case 'Text':
      return <Text {...props} />;
    case 'Table':
      return <Table {...props} />;
    default:
      return <div>Unknown component type</div>;
  }
};

export default ComponentRenderer; 