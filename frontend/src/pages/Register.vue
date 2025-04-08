<template>
  <div class="pt-16 pb-10 bg-neutral min-h-screen px-4">
    <div class="max-w-xl mx-auto bg-white p-6 rounded shadow">
      <h2 class="text-2xl font-bold text-primary mb-6 text-center">Register as</h2>

      <div class="flex justify-center space-x-4 mb-6">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          :class="[
            'px-4 py-2 rounded font-medium',
            activeTab === tab
              ? 'bg-primary text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          ]"
        >
          {{ tab }}
        </button>
      </div>

      <component :is="tabComponents[activeTab]" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import RegisterBuyerForm from '../components/form/RegisterBuyerForm.vue'
import RegisterIndividualForm from '../components/form/RegisterIndividualForm.vue'
import RegisterCompanyForm from '../components/form/RegisterCompanyForm.vue'

const tabs = ['Buyer', 'Individual Seller', 'Company Seller']
const activeTab = ref('Buyer')

const tabComponents = {
  Buyer: RegisterBuyerForm,
  'Individual Seller': RegisterIndividualForm,
  'Company Seller': RegisterCompanyForm
}
</script>

<script>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
export default {
  layout: DefaultLayout,
}
</script>
