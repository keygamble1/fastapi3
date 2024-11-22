<script>
    export let error
</script>

{#if typeof error.detail==='string'}
    <div
        class="alert alert-danger"
        role="alert"
    >
    {error.detail}
    </div>
    
 
{:else if typeof error.detail ==='object' && error.detail.length>0}

        <div
            class="alert alert-danger"
            role="alert"
        >
        {#each error.detail as err,i}
        <div>
            <strong>{err.loc[1]}</strong> :{err.msg}
            <!-- loc= 배열의 두번째요소 0이 첫번째 
             err.loc={'fieldname','invald'} 면 invalid가져옴-->
            <!-- 콜론 :의미있는게아니고 그냥 string임 -->
             <!-- loc:[field,invalid] err:msg 이런식으로 되어있을거 -->
        </div>
        {/each}
        </div>
        
        



{/if}