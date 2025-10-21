<script>

    import { stor } from './x.svelte.js';
	import {get} from "svelte/store";

    function click()
    {
        stor.update(v => v + 1);
        console.log('stor after click:', $stor);
    }

    let ddd = $derived.by(() => {
		return {a:stor, b: get(stor), c: $stor};
	});


</script>


<button onclick={click}>Click me</button>


<p>State value: {JSON.stringify($stor)}</p>
<p>ddd value: {JSON.stringify(ddd)}</p>