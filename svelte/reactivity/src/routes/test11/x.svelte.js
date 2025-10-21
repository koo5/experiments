import {writable} from "svelte/store";

export let stor = writable(0);

export default { stor };