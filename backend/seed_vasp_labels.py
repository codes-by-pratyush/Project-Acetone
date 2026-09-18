from backend.app.database import engine, Base, SessionLocal
from backend.app.models.vasp import VASPLabel

# Pre-seeded curated intelligence for hackathon demo (Binance, CoinDCX, WazirX, Coinbase)
CURATED_VASP_RECORDS = [
    {
        "address": "0x28c6c06298d514db089934071355e5743bf21d60",
        "vasp_name": "Binance 14",
        "category": "hot_wallet",
        "chain": "ethereum",
        "confidence_score": 0.96,
        "source": "Etherscan Verified Labels"
    },
    {
        "address": "0x21a31ee1afc51d94c2efccaa2092ad1028285549",
        "vasp_name": "Binance 15",
        "category": "hot_wallet",
        "chain": "ethereum",
        "confidence_score": 0.95,
        "source": "Etherscan Verified Labels"
    },
    {
        "address": "0x708396c0ba02534c0e03482622b4666293c12637",
        "vasp_name": "CoinDCX Hot Wallet",
        "category": "hot_wallet",
        "chain": "ethereum",
        "confidence_score": 0.92,
        "source": "Open Threat Intel / State Cyber Cell Dataset"
    },
    {
        "address": "0x56ed30e386007e4d6b7f87ca68163b4b001d8604",
        "vasp_name": "WazirX Primary Hot Wallet",
        "category": "hot_wallet",
        "chain": "ethereum",
        "confidence_score": 0.91,
        "source": "Public Forensic Disclosures"
    },
    {
        "address": "0x71660c4005ba85c37ccec55d0c4493e66fe775d3",
        "vasp_name": "Coinbase 2",
        "category": "hot_wallet",
        "chain": "ethereum",
        "confidence_score": 0.98,
        "source": "Etherscan Verified Labels"
    }
]

def seed_vasp_intelligence():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    inserted = 0
    try:
        for rec in CURATED_VASP_RECORDS:
            existing = db.query(VASPLabel).filter(VASPLabel.address == rec["address"]).first()
            if not existing:
                vasp_entry = VASPLabel(**rec)
                db.add(vasp_entry)
                inserted += 1
        db.commit()
        print(f"=== T-M4-08: Successfully seeded {inserted} new VASP exchange records ===")
    except Exception as e:
        db.rollback()
        print(f"FAILED to seed VASP intelligence. Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_vasp_intelligence()