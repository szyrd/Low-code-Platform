export interface ComponentProps {
  label?: string;
  color?: string;
  placeholder?: string;
  value?: string;
  data?: any[];
  columns?: { key: string; header: string }[];
  [key: string]: any;
}

export interface ComponentData {
  id: string;
  type: 'Button' | 'Input' | 'Text' | 'Table';
  x: number;
  y: number;
  w: number;
  h: number;
  props: ComponentProps;
}

export interface LayoutData {
  components: ComponentData[];
  name: string;
} 