import { defineStore } from 'pinia'
import type { ChatMessage, ChatResponse } from '~/types'
import { useSourceStore } from '~/stores/sources'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as ChatMessage[],
    notes: [] as string[],
    loading: false,
    error: '',
    backendStatus: '',
  }),

  actions: {
    async checkHealth() {
      const api = useApi()

      try {
        const result = await api.healthCheck() as { status: string; openai_configured: boolean }
        this.backendStatus = result.openai_configured
          ? 'Backend verbunden'
          : 'Backend laeuft, aber OpenAI-Key fehlt'
      } catch {
        this.backendStatus = 'Backend nicht erreichbar'
      }
    },

    async sendMessage(content: string) {
      const api = useApi()
      const sourceStore = useSourceStore()

      if (!content.trim()) return

      this.loading = true
      this.error = ''

      this.messages.push({
        id: crypto.randomUUID(),
        role: 'user',
        content,
      })

      try {
        const response = await api.sendChatMessage({
          message: content,
          source_ids: sourceStore.selectedIds,
        }) as ChatResponse

        this.messages.push({
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response.answer,
        })

        this.notes = response.notes
      } catch (error) {
        this.error =
          error instanceof Error ? error.message : 'Chat-Anfrage fehlgeschlagen.'
      } finally {
        this.loading = false
      }
    },
  },
})
