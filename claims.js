const { ethers } = require('/home/agent/work/wallet/node_modules/ethers');
const fs=require('fs');
const P='0x5555fa783936c260f77385b4e153b9725fef1719';
const IFACE=new ethers.Interface([
 'event ClaimCreated(uint256 indexed id, address indexed issuer, uint256 indexed bountyId, address bountyIssuer, string title, string description, uint256 createdAt, string imageUri, uint256 round)',
 'event VotingStarted(uint256 indexed bountyId, uint256 indexed claimId, uint256 deadline, uint256 issuerYesWeight, uint256 round)',
 'event BountyJoined(uint256 indexed bountyId, address indexed participant, uint256 amount, uint256 latestBountyBalance, uint256 round)']);
const T=n=>IFACE.getEvent(n).topicHash;
const PAD=ethers.zeroPadValue(ethers.toBeHex(143),32);
(async()=>{
 const p=new ethers.JsonRpcProvider('https://arb1.arbitrum.io/rpc',42161,{staticNetwork:true});
 const tip=await p.getBlockNumber();
 const START=tip-3_000_000, STEP=250_000;
 const out={tip,claims:[],votes:[],joins:[]};
 for(let f=START; f<=tip; f+=STEP){
  const t=Math.min(f+STEP-1,tip);
  const q=async(topics)=>{for(let a=0;a<4;a++){try{return await p.getLogs({address:P,fromBlock:f,toBlock:t,topics});}catch(e){if(a==3){console.error('SKIP',f,(e.shortMessage||e.message).slice(0,80));return null;}await new Promise(r=>setTimeout(r,1500));}}};
  for(const [k,topics] of [['claims',[T('ClaimCreated'),null,null,PAD]],['votes',[T('VotingStarted'),PAD]],['joins',[T('BountyJoined'),PAD]]]){
   const ls=await q(topics); if(ls===null){out.incomplete=true;continue;}
   for(const l of ls){const d=IFACE.parseLog(l);
    if(k==='claims') out.claims.push({id:Number(d.args.id),issuer:d.args.issuer,t:Number(d.args.createdAt),title:d.args.title,uri:d.args.imageUri,desc:d.args.description});
    if(k==='votes') out.votes.push({claimId:Number(d.args.claimId),deadline:Number(d.args.deadline)});
    if(k==='joins') out.joins.push({who:d.args.participant,amt:ethers.formatEther(d.args.amount),bal:ethers.formatEther(d.args.latestBountyBalance),blk:l.blockNumber});}
  }
  console.error(`${f}-${t}  claims=${out.claims.length} joins=${out.joins.length}`);
 }
 fs.writeFileSync('/home/agent/work/c143survey/onchain143.json',JSON.stringify(out,null,1));
 console.log('TOTAL claims',out.claims.length,'joins',out.joins.length,'votingStarted',out.votes.length,'incomplete',!!out.incomplete);
})();
