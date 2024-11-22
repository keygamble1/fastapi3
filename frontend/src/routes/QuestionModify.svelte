<script>
	import { push } from 'svelte-spa-router';
	import Error from "../components/Error.svelte";
	import fastapi from "../lib/api";
  let error={detail:[]}
  let subject=''
  let content=''
  export let params={}
  const question_id=params.question_id
  fastapi('get',"/api/question/detail/"+question_id,{},
  (json)=>{
    subject=json.subject
    content=json.content
  })
  function update_question(event){
    event.preventDefault()  
    let url="/api/question/update"
    let params={
        subject:subject,
        content:content,
        question_id:question_id
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
    <h5 class="border-bottom pb-2">질문수정</h5>
    <Error error={error}/>
    <form  method="post" class="my-3">
        <div class="my-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value={subject}>
        </div>
        <div class="my-3">
            <label for="content">내용</label>
            <textarea  class="form-control" rows="10" bind:value={content}></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_question}">수정하기</button>
    </form>
</div>
