export async function startGame() {
    const res = await fetch(`/api/start_game`, {
        method: 'POST',
    });
    return res;
}

export async function getMoves(queryString: string){
    const res = await fetch('/api/getMoves', {
        method: 'GET',
        body: queryString,
    })
    return res;
}