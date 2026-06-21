<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useChatStore } from "~/stores/chat";
import { useSourceStore } from "~/stores/sources";

const chatStore = useChatStore();
const sourceStore = useSourceStore();
const input = ref("");

onMounted(() => {
  chatStore.checkHealth();
});

async function handleSend() {
  const value = input.value.trim();
  if (!value) return;

  await chatStore.sendMessage(value);
  input.value = "";
}

async function onKeydown(event: KeyboardEvent) {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    await handleSend();
  }
}
</script>

<template>
  <section class="panel chat-panel">
    <div class="panel-header">
      <h2>Chat</h2>
      <p>{{ sourceStore.selectedIds.length }} Quellen aktiv</p>
      <p class="status-text">{{ chatStore.backendStatus }}</p>
    </div>

    <div class="chat-messages">
      <div v-if="chatStore.messages.length === 0" class="empty-state">
        Stelle eine Frage zu den ausgewaehlten Quellen.
      </div>

      <div
        v-for="message in chatStore.messages"
        :key="message.id"
        class="message"
        :class="message.role"
      >
        <div class="message-role">
          {{ message.role === "user" ? "Du" : "Assistent" }}
        </div>
        <div class="message-content">{{ message.content }}</div>
      </div>

      <div v-if="chatStore.loading" class="message assistant">
        <div class="message-role">Assistent</div>
        <div class="message-content">Denke nach...</div>
      </div>
    </div>

    <p v-if="chatStore.error" class="error">{{ chatStore.error }}</p>

    <div class="chat-input">
      <textarea
        v-model="input"
        rows="3"
        placeholder="Frage zu den Quellen stellen..."
        @keydown="onKeydown"
      />
      <button
        :disabled="chatStore.loading || sourceStore.selectedIds.length === 0"
        @click="handleSend"
      >
        Senden
      </button>
    </div>
  </section>
</template>
