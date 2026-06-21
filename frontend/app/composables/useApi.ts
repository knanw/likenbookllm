export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const fetchSources = async () => {
    return await $fetch('/sources', {
      baseURL,
    })
  }

  const createSource = async (payload: { title: string; content: string }) => {
    return await $fetch('/sources', {
      method: 'POST',
      body: payload,
      baseURL,
    })
  }

  const deleteSource = async (sourceId: string) => {
    return await $fetch(`/sources/${sourceId}`, {
      method: 'DELETE',
      baseURL,
    })
  }

  const sendChatMessage = async (payload: {
    message: string
    source_ids: string[]
  }) => {
    return await $fetch('/chat', {
      method: 'POST',
      body: payload,
      baseURL,
    })
  }

  const healthCheck = async () => {
    return await $fetch('/health', {
      baseURL,
    })
  }

  return {
    fetchSources,
    createSource,
    deleteSource,
    sendChatMessage,
    healthCheck,
  }
}
