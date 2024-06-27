export interface Express {
  options(arg0: string, arg1: (req: import("cors").CorsRequest, res: { statusCode?: number | undefined; setHeader(key: string, value: string): any; end(): any; }, next: (err?: any) => any) => void): unknown;
  use: (arg?: any, otherArg?: any) => any;
  listen: (arg?: any, otherArg?: any) => any;
}

export interface Router {
  get: (path?: string, params?: any) => void;
  post: (path?: string, params?: any) => void;
}

export interface Request {
  cookies?: Cookies;
  cookie?: Cookies;
  user?: any;
  body?: any;
  headers?: any;
}

export interface Response {
  send: (text: string) => void;
  status: (number: number) => any;
  cookie: (jwt: string, token: string, durationCookie: DurationCookie) => any;
  clearCookie: (token: string) => any;
}

export interface TypeOptions {
  useNewUrlParser: boolean;
  useUnifiedTopology: boolean;
}

export interface Cookies {
  jwt: string;
}

export interface DurationCookie {
  maxAge: number;
}
