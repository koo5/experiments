<script>

    import { st } from './x.svelte.js';


	if (typeof window !== 'undefined')
	{
	}

    function click()
    {
        st.a.n = st.a.n + 1;
        console.log('st after click:', $state.snapshot(st), typeof st);
        window.st = st;


    }


</script>


<button onclick={click}>Click me</button>


<p>State value: {JSON.stringify(st)}</p>
