export class Agent {
  id?: string;
  name?: string;
  role?: string;
  goals: string[] = [];
  config?: string;
  chatHistory?: any;
}
