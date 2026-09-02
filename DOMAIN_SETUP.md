# Domain Setup: GoDaddy to Vercel

This guide walks you through connecting your GoDaddy domain to your Vercel-hosted Salaama Eats website.

## Prerequisites

- A domain registered on GoDaddy (e.g., `salamaeats.ca`, `salamaeats.com`)
- Your website deployed on Vercel
- Access to both GoDaddy and Vercel dashboards

## Step 1: Add Domain to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project (Salaama Eats)
3. Navigate to **Settings** → **Domains**
4. Click **Add Domain**
5. Enter your domain (e.g., `salamaeats.com`)
6. Choose "Use Nameservers" as the connection method

Vercel will display nameservers you need to add to GoDaddy:
- **ns1.vercel.com**
- **ns2.vercel.com**
- **ns3.vercel.com**
- **ns4.vercel.com**

## Step 2: Update Nameservers in GoDaddy

1. Go to [GoDaddy Dashboard](https://www.godaddy.com/dashboard)
2. Find your domain in the **My Products** section
3. Click the domain to open its management page
4. Look for **Nameservers** section
5. Select **Change Nameservers**
6. Choose **I'll use other nameservers**
7. Replace the existing nameservers with Vercel's:
   - `ns1.vercel.com`
   - `ns2.vercel.com`
   - `ns3.vercel.com`
   - `ns4.vercel.com`
8. Click **Save**

**Important:** DNS changes can take 24-48 hours to propagate. Your site will redirect to Vercel once propagation is complete.

## Step 3: Verify Domain in Vercel (Optional)

You can verify the domain is working before full propagation:

1. Return to Vercel → **Settings** → **Domains**
2. Your domain should show **Pending** initially
3. Once DNS propagates, it will show **Valid Configuration**

## Step 4: Add Additional Subdomains (Optional)

If you want `www.salamaeats.com` to work as well:

1. In Vercel domain settings, add `www.salamaeats.com` as an additional domain
2. Select **Redirect to Domain**
3. Choose your main domain to redirect to

Vercel automatically handles www redirects with the nameserver setup.

## Step 5: Enable HTTPS

Vercel automatically provisions and renews SSL certificates for your domain:

1. After DNS propagates, check **Settings** → **Domains**
2. Your domain should show a green checkmark
3. All traffic is automatically redirected to HTTPS

## Troubleshooting

### Domain still shows pending after 24 hours
- Verify the nameservers are correctly set in GoDaddy
- Use a tool like [MX Toolbox](https://mxtoolbox.com/nslookup.aspx) to check nameserver propagation
- Clear your browser cache

### DNS propagation checker
- Check status at [whatsmydns.net](https://www.whatsmydns.net/)
- Enter your domain and look for nameserver records

### Need to revert to GoDaddy nameservers
1. Go back to GoDaddy domain settings
2. Select **Change Nameservers**
3. Choose **I'll use GoDaddy nameservers**
4. This will revert but may take 24-48 hours

## Email Setup (Optional)

If you have email at your domain (e.g., contact@salamaeats.com):

1. Keep email services pointing to GoDaddy nameservers separately, OR
2. Set up email forwarding with Vercel if using third-party email
3. Add MX records manually in Vercel's DNS settings for your domain

## Next Steps

Once your domain is connected:

1. Test the site loads correctly on both:
   - `salamaeats.com`
   - `www.salamaeats.com`

2. Update any hardcoded URLs in your site to use the new domain

3. Set up SSL certificate monitoring (Vercel handles this automatically)

4. Consider setting up DNS records for email if needed

## Support

- **Vercel Docs**: https://vercel.com/docs/concepts/projects/domains
- **GoDaddy Support**: https://www.godaddy.com/help
