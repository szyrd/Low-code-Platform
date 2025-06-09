import React from 'react';
import { ComponentProps } from '../types/types';

export const Button: React.FC<ComponentProps> = ({ label = 'Button', color = 'blue', onClick }) => {
  return (
    <button 
      style={{ 
        backgroundColor: color, 
        color: 'white', 
        padding: '8px 16px', 
        border: 'none', 
        borderRadius: '4px', 
        cursor: 'pointer' 
      }}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export const Input: React.FC<ComponentProps> = ({ placeholder = 'Enter text...', value = '', onChange }) => {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      style={{ 
        padding: '8px', 
        borderRadius: '4px', 
        border: '1px solid #ccc', 
        width: '100%' 
      }}
    />
  );
};

export const Text: React.FC<ComponentProps> = ({ value = 'Text', color = 'black' }) => {
  return (
    <div style={{ color }}>
      {value}
    </div>
  );
};

export const Table: React.FC<ComponentProps> = ({ 
  data = [], 
  columns = [{ key: 'id', header: 'ID' }, { key: 'name', header: 'Name' }] 
}) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {columns.map((col) => (
              <td key={col.key} style={{ border: '1px solid #ddd', padding: '8px' }}>
                {row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}; 