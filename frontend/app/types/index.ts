export interface SourceItem {
  id: string
  title: string
  content: string
  created_at: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
}

export interface ChatResponse {
  answer: string
  notes: string[]
}
