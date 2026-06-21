import { defineStore } from 'pinia'
import type { SourceItem } from '~/types'

export const useSourceStore = defineStore('sources', {
  state: () => ({
    items: [] as SourceItem[],
    selectedIds: [] as string[],
    loading: false,
    error: '',
  }),

  actions: {
    async loadSources() {
      const api = useApi()
      this.loading = true
      this.error = ''

      try {
        const data = await api.fetchSources() as SourceItem[]
        this.items = data

        if (this.selectedIds.length === 0) {
          this.selectedIds = data.map((item) => item.id)
        }
      } catch (error) {
        this.error =
          error instanceof Error ? error.message : 'Quellen konnten nicht geladen werden.'
      } finally {
        this.loading = false
      }
    },

    async addSource(title: string, content: string) {
      const api = useApi()
      const newSource = await api.createSource({ title, content }) as SourceItem
      this.items.unshift(newSource)
      this.selectedIds.push(newSource.id)
    },

    async removeSource(sourceId: string) {
      const api = useApi()
      await api.deleteSource(sourceId)
      this.items = this.items.filter((item) => item.id !== sourceId)
      this.selectedIds = this.selectedIds.filter((id) => id !== sourceId)
    },

    toggleSelection(sourceId: string) {
      if (this.selectedIds.includes(sourceId)) {
        this.selectedIds = this.selectedIds.filter((id) => id !== sourceId)
      } else {
        this.selectedIds.push(sourceId)
      }
    },
  },
})
