import React, { ReactNode, useState } from 'react';

interface TabsProps {
  defaultValue?: number;
  children: ReactNode;
}

export const Tabs: React.FC<TabsProps> = ({ defaultValue = 0, children }) => {
  const [activeTab, setActiveTab] = useState(defaultValue);
  
  return (
    <div className="tabs">
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child) && child.type === TabsList) {
          return React.cloneElement(child as React.ReactElement<any>, {
            activeTab,
            setActiveTab,
          });
        }
        
        if (React.isValidElement(child) && child.type === TabsContent) {
          return React.cloneElement(child as React.ReactElement<any>, {
            activeTab,
          });
        }
        
        return child;
      })}
    </div>
  );
};

interface TabsListProps {
  children: ReactNode;
  activeTab?: number;
  setActiveTab?: (index: number) => void;
}

export const TabsList: React.FC<TabsListProps> = ({ children, activeTab, setActiveTab }) => {
  return (
    <div className="tabs-list flex border-b border-gray-200 mb-4">
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child) && child.type === TabsTrigger) {
          return React.cloneElement(child as React.ReactElement<any>, {
            index,
            active: index === activeTab,
            onClick: () => setActiveTab && setActiveTab(index),
          });
        }
        
        return child;
      })}
    </div>
  );
};

interface TabsTriggerProps {
  children: ReactNode;
  index?: number;
  active?: boolean;
  onClick?: () => void;
}

export const TabsTrigger: React.FC<TabsTriggerProps> = ({ children, active, onClick }) => {
  return (
    <button
      className={`px-4 py-2 text-sm font-medium transition-colors ${
        active
          ? 'text-blue-600 border-b-2 border-blue-600'
          : 'text-gray-600 hover:text-blue-500'
      }`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

interface TabsContentProps {
  children: ReactNode;
  value: number;
  activeTab?: number;
}

export const TabsContent: React.FC<TabsContentProps> = ({ children, value, activeTab }) => {
  if (value !== activeTab) return null;
  
  return <div className="tabs-content">{children}</div>;
};

export default { Tabs, TabsList, TabsTrigger, TabsContent }; 