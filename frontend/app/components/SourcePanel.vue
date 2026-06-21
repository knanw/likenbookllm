<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useSourceStore } from "~/stores/sources";

const sourceStore = useSourceStore();

const title = ref("");
const content = ref("");
const submitting = ref(false);

onMounted(() => {
  sourceStore.loadSources();
});

async function handleSubmit() {
  if (!title.value.trim() || !content.value.trim()) return;

  submitting.value = true;

  try {
    await sourceStore.addSource(title.value, content.value);
    title.value = "";
    content.value = "";
  } catch (error) {
    console.error(error);
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <section class="panel">
    <div class="panel-header">
      <h2>Quellen</h2>
      <p>Texte hinzufuegen und fuer den Chat auswaehlen.</p>
    </div>

    <form class="source-form" @submit.prevent="handleSubmit">
      <input v-model="title" type="text" placeholder="Titel der Quelle" />
      <textarea
        v-model="content"
        rows="5"
        placeholder="Text oder Zusammenfassung einfuegen"
      />
      <button type="submit" :disabled="submitting">
        {{ submitting ? "Speichert..." : "Quelle hinzufuegen" }}
      </button>
    </form>

    <p v-if="sourceStore.error" class="error">{{ sourceStore.error }}</p>
    <p v-if="sourceStore.loading" class="muted">Lade Quellen...</p>

    <ul class="source-list">
      <li v-for="item in sourceStore.items" :key="item.id" class="source-card">
        <label class="source-select">
          <input
            type="checkbox"
            :checked="sourceStore.selectedIds.includes(item.id)"
            @change="sourceStore.toggleSelection(item.id)"
          />
          <span>{{ item.title }}</span>
        </label>

        <p class="source-content">{{ item.content }}</p>

        <button
          class="danger-button"
          @click="sourceStore.removeSource(item.id)"
        >
          Loeschen
        </button>
      </li>
    </ul>
  </section>
</template>
