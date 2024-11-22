<script>

  import { push } from 'svelte-spa-router';
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
  let subject=""
  let content=""
  let error={detail:[]}
// 그냥링크만들어가서 push하면 저절로 post가되나? 확인
// 요청이라는게 post get이라는거 url에 post,get,delete든 실행하면 조회되거나 실행되거나 등등됨

  function post_question(event){
    event.preventDefault()
    let url="/api/question/create"
    let params={
        subject:subject,
        content:content,
    }
    fastapi('post',url,params,
        (json)=>{
            push("/")
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
    <h5 class="border-bottom pb-2">질문등록</h5>
    <Error error={error}/>
    <form  method="post" class="my-3">
        <div class="my-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value={subject}>

        </div>
        <div class="mb-3 ">
            <label for="content">내용</label>
            <textarea class="form-control" rows="15" bind:value={content}></textarea>
        </div>
        <button type="submit" class="btn btn-primary" on:click="{post_question}" >저장하기</button>
    </form>
</div>

