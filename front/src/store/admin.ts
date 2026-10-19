// Utilities
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { checkPassword } from '@/api/admin'

// the password is only kept for the current tab (sessionStorage)
const PASSWORD_KEY = 'ornipedia.admin'

function readPassword(): string {
  try {
    return window.sessionStorage.getItem(PASSWORD_KEY) ?? ''
  } catch {
    return ''
  }
}

export type LoginError = 'invalid' | 'disabled' | 'network'

export const useAdminStore = defineStore('admin', () => {
  const password = ref(readPassword())
  const loggedIn = computed(() => password.value != '')

  // returns null when logged in, the reason of the failure otherwise
  async function login(candidate: string): Promise<LoginError | null> {
    try {
      await checkPassword(candidate)
    } catch (err: unknown) {
      const status = (err as { response?: { status?: number } }).response?.status
      return status == 401 ? 'invalid' : status == 503 ? 'disabled' : 'network'
    }
    password.value = candidate
    try {
      window.sessionStorage.setItem(PASSWORD_KEY, candidate)
    } catch {
      // only kept in memory
    }
    return null
  }

  function logout() {
    password.value = ''
    try {
      window.sessionStorage.removeItem(PASSWORD_KEY)
    } catch {
      // nothing stored
    }
  }

  return { password, loggedIn, login, logout }
})
