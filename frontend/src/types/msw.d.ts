declare module 'msw' {
  export const rest: any;
  export const graphql: any;
  export const setupWorker: any;
}

declare module 'msw/node' {
  export const setupServer: any;
} 