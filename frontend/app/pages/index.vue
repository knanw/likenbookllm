<script setup lang="ts">
import SourcePanel from "~/components/SourcePanel.vue";
import ChatPanel from "~/components/ChatPanel.vue";
import NotesPanel from "~/components/NotesPanel.vue";
</script>

<template>
  <div class="app-layout">
    <aside class="left-column">
      <SourcePanel />
    </aside>

    <main class="center-column">
      <ChatPanel />
    </main>

    <aside class="right-column">
      <NotesPanel />
    </aside>
  </div>
</template>
