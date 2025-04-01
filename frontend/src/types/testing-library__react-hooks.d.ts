declare module '@testing-library/react-hooks' {
  export function renderHook<Result, Props>(
    callback: (props: Props) => Result,
    options?: {
      initialProps?: Props;
      wrapper?: React.ComponentType<{ children: React.ReactNode }>;
    }
  ): {
    result: { current: Result };
    waitFor: (callback: () => boolean | void, options?: { timeout?: number }) => Promise<void>;
    waitForNextUpdate: (options?: { timeout?: number }) => Promise<void>;
    waitForValueToChange: (selector: () => any, options?: { timeout?: number }) => Promise<void>;
    rerender: (props?: Props) => void;
    unmount: () => void;
  };

  export function act(callback: () => void | Promise<void>): Promise<void>;
} 