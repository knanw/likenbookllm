<script setup lang="ts">
import { useChatStore } from "~/stores/chat";

const chatStore = useChatStore();
</script>

<template>
  <section class="panel">
    <div class="panel-header">
      <h2>Notizen</h2>
      <p>Kurzuebersicht der letzten Antwort.</p>
    </div>

    <div v-if="chatStore.notes.length === 0" class="empty-state">
      Nach der ersten Modellantwort erscheinen hier Notizen.
    </div>

    <ul v-else class="notes-list">
      <li
        v-for="(note, index) in chatStore.notes"
        :key="index"
        class="note-card"
      >
        {{ note }}
      </li>
    </ul>
  </section>
</template>
