import React from 'react';

interface IconProps {
  className?: string;
}

export const EnvelopeIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M17.5 4.375H2.5C2.15833 4.375 1.875 4.65833 1.875 5V15C1.875 15.3417 2.15833 15.625 2.5 15.625H17.5C17.8417 15.625 18.125 15.3417 18.125 15V5C18.125 4.65833 17.8417 4.375 17.5 4.375Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M3.75 6.25L10 10.625L16.25 6.25" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const LockIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M15.8333 9.16667H4.16667C3.24619 9.16667 2.5 9.91286 2.5 10.8333V16.6667C2.5 17.5871 3.24619 18.3333 4.16667 18.3333H15.8333C16.7538 18.3333 17.5 17.5871 17.5 16.6667V10.8333C17.5 9.91286 16.7538 9.16667 15.8333 9.16667Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M5.83333 9.16667V5.83333C5.83333 4.72827 6.27232 3.66846 7.05372 2.88706C7.83512 2.10565 8.89493 1.66667 10 1.66667C11.1051 1.66667 12.1649 2.10565 12.9463 2.88706C13.7277 3.66846 14.1667 4.72827 14.1667 5.83333V9.16667" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const EyeIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M10 4.16667C3.75 4.16667 1.25 10 1.25 10C1.25 10 3.75 15.8333 10 15.8333C16.25 15.8333 18.75 10 18.75 10C18.75 10 16.25 4.16667 10 4.16667Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M10 13.3333C11.8409 13.3333 13.3333 11.8409 13.3333 10C13.3333 8.15905 11.8409 6.66667 10 6.66667C8.15905 6.66667 6.66667 8.15905 6.66667 10C6.66667 11.8409 8.15905 13.3333 10 13.3333Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const EyeSlashIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M11.7667 11.7667C11.5428 12.0089 11.2691 12.2025 10.9654 12.335C10.6617 12.4676 10.3342 12.5367 10.0021 12.5384C9.67001 12.5402 9.34178 12.4744 9.03666 12.345C8.73154 12.2157 8.45575 12.0251 8.22921 11.7853C8.00268 11.5456 7.82713 11.2598 7.70455 10.9473C7.58197 10.6349 7.5185 10.3021 7.52271 9.96662C7.52691 9.63118 7.6 9.29999 7.7346 8.99148C7.86921 8.68297 8.05366 8.40335 8.28334 8.16667M14.95 14.95C13.5255 16.0358 11.7909 16.6373 10 16.6667C4.16667 16.6667 1.25 10 1.25 10C2.34931 7.78028 3.91169 5.86612 5.8 4.38334L14.95 14.95ZM8.25 3.53334C8.82005 3.38829 9.40823 3.31415 10 3.31417C15.8333 3.31417 18.75 10 18.75 10C18.1842 11.0656 17.477 12.058 16.65 12.95L8.25 3.53334Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M1.25 1.25L18.75 18.75" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const UserIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M16.6667 17.5V15.8333C16.6667 14.9493 16.3155 14.1014 15.6904 13.4763C15.0652 12.8512 14.2174 12.5 13.3333 12.5H6.66667C5.78261 12.5 4.93476 12.8512 4.30964 13.4763C3.68452 14.1014 3.33333 14.9493 3.33333 15.8333V17.5" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M10 9.16667C11.8409 9.16667 13.3333 7.67428 13.3333 5.83333C13.3333 3.99238 11.8409 2.5 10 2.5C8.15905 2.5 6.66667 3.99238 6.66667 5.83333C6.66667 7.67428 8.15905 9.16667 10 9.16667Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const CheckIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M16.6667 5L7.50004 14.1667L3.33337 10" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const CrossIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="20" 
    height="20" 
    viewBox="0 0 20 20" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M11.25 8.75L8.75 11.25M8.75 8.75L11.25 11.25M17.5 10C17.5 10.9849 17.306 11.9602 16.9291 12.8701C16.5522 13.7801 15.9997 14.6069 15.3033 15.3033C14.6069 15.9997 13.7801 16.5522 12.8701 16.9291C11.9602 17.306 10.9849 17.5 10 17.5C9.01509 17.5 8.03982 17.306 7.12987 16.9291C6.21993 16.5522 5.39314 15.9997 4.6967 15.3033C4.00026 14.6069 3.44781 13.7801 3.0709 12.8701C2.69399 11.9602 2.5 10.9849 2.5 10C2.5 8.01088 3.29018 6.10322 4.6967 4.6967C6.10322 3.29018 8.01088 2.5 10 2.5C11.9891 2.5 13.8968 3.29018 15.3033 4.6967C16.7098 6.10322 17.5 8.01088 17.5 10Z" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
);

export const LogoIcon: React.FC<IconProps> = ({ className }) => (
  <svg 
    className={className}
    width="64" 
    height="64" 
    viewBox="0 0 64 64" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
  >
    <path 
      d="M32 5.33334L32 58.6667" 
      stroke="#CCE4F6" 
      strokeWidth="4" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M16 21.3333L32 5.33334L48 21.3333" 
      stroke="#CCE4F6" 
      strokeWidth="4" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
    <path 
      d="M16 42.6667H48" 
      stroke="#F4D58D" 
      strokeWidth="4" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    />
  </svg>
); 