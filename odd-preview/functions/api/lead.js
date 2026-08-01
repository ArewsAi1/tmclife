export async function onRequestPost(context) {
  try {
    const request = context.request;
    const contentType = request.headers.get('content-type') || '';
    let data;
    if (contentType.includes('application/json')) data = await request.json();
    else data = Object.fromEntries((await request.formData()).entries());

    if (data.website) return Response.json({ok:true});
    const name = String(data.name || '').trim();
    const phone = String(data.phone || '').trim();
    const email = String(data.email || '').trim();
    if (!name || (!phone && !email)) return Response.json({ok:false,error:'Please provide your name and a phone number or email.'},{status:400});

    await context.env.LEADS_DB.prepare(`INSERT INTO leads (lead_type,name,email,phone,city,project_type,message,source_url,user_agent) VALUES (?,?,?,?,?,?,?,?,?)`)
      .bind(
        String(data.lead_type || 'general').slice(0,80),
        name.slice(0,150),
        email.slice(0,200),
        phone.slice(0,80),
        String(data.city || '').slice(0,120),
        String(data.project_type || '').slice(0,160),
        String(data.message || '').slice(0,4000),
        String(data.source_url || request.headers.get('referer') || '').slice(0,500),
        String(request.headers.get('user-agent') || '').slice(0,500)
      ).run();

    return Response.json({ok:true,message:'Thanks — your request was received.'});
  } catch (error) {
    return Response.json({ok:false,error:'We could not save your request. Please call (435) 222-5819.'},{status:500});
  }
}

export function onRequestGet() {
  return Response.json({ok:true,service:'Ogden Deck Depot lead intake'});
}
