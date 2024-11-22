<script>
	import { push } from 'svelte-spa-router';
	import Error from "../components/Error.svelte";
	import fastapi from "../lib/api";
    export let params={}
  let error={detail:[]}
  let content=''
  let question_id=0
 
  const answer_id=params.answer_id
  fastapi('get',"/api/answer/detail/"+answer_id,{},
    (json)=>{
        question_id =json.question_id 
        content=json.content
    })
  function update_answer(event){
    event.preventDefault()  
    let url="/api/answer/update"
    let params={
        answer_id:answer_id,
        content:content,
        
    }
    fastapi('put',url,params,
        (json)=>{
            push('/detail/'+question_id)
        },
        (err_json)=>{
            error=err_json
        }
    )

  }
</script>
<div
    class="container"
>
    <h5 class="border-bottom pb-2">답변수정</h5>
    <Error error={error}/>
    <form  method="post" class="my-3">
        <div class="my-3">
            <label for="content">내용</label>
            <textarea  class="form-control" rows="10" bind:value={content}></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_answer}">수정하기</button>
    </form>
</div>
